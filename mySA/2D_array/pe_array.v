
module ram(
    input clk,
    input we,
    input  logic unsigned [DATA_WIDTH-1:0] din,
    input  logic unsigned [ADDR_WIDTH-1:0] addr,
    output logic unsigned [DATA_WIDTH-1:0] dout
);
    parameter integer DATA_WIDTH = 10;
    parameter integer ADDR_WIDTH = 4;

    logic unsigned [DATA_WIDTH-1:0] mem [(2**ADDR_WIDTH)-1:0];

    always_ff @(posedge clk) begin
        if (we) begin
            mem[addr] <= din;
        end
        dout <= mem[addr];
    end

endmodule

module array #(
    parameter integer NUM_PES = 4,
    parameter integer DATA_WIDTH = 10,
    parameter integer ADDR_WIDTH = 4
)(
    input  logic clk,
    input  logic compute,
    input  logic init,

    // RAM A: one DATA_WIDTH word per address, feeds the first PE
    input  logic we_a,
    input  logic unsigned [ADDR_WIDTH-1:0] addr_a,
    input  logic unsigned [DATA_WIDTH-1:0] din_a,

    // RAM B: one word per address holding the B value of every PE
    // (PE i uses bits [i*DATA_WIDTH +: DATA_WIDTH])
    input  logic we_b,
    input  logic unsigned [ADDR_WIDTH-1:0] addr_b,
    input  logic unsigned [NUM_PES*DATA_WIDTH-1:0] din_b,

    output logic unsigned [DATA_WIDTH-1:0] array_output
);

    logic unsigned [DATA_WIDTH-1:0] pe_outputs [NUM_PES-1:0][NUM_PES-1:0];

    logic unsigned [NUM_PES*DATA_WIDTH-1:0]         input_a;
    logic unsigned [NUM_PES*DATA_WIDTH-1:0] ram_b_dout;
    logic unsigned [DATA_WIDTH-1:0]         input_b [NUM_PES-1:0];

    ram #(
        .DATA_WIDTH(DATA_WIDTH),
        .ADDR_WIDTH(ADDR_WIDTH)
    ) ram_a (
        .clk  (clk),
        .we   (we_a),
        .din  (din_a),
        .addr (addr_a),
        .dout (input_a)
    );

    ram #(
        .DATA_WIDTH(NUM_PES*DATA_WIDTH),
        .ADDR_WIDTH(ADDR_WIDTH)
    ) ram_b (
        .clk  (clk),
        .we   (we_b),
        .din  (din_b),
        .addr (addr_b),
        .dout (ram_b_dout)
    );

    genvar i;

    generate
        for (i = 0; i < NUM_PES; i++) begin : gen_unpack_b
            assign input_b[i] = ram_b_dout[i*DATA_WIDTH +: DATA_WIDTH];
        end
    endgenerate

    generate
        for (i = 0; i < NUM_PES; i++) begin : gen_pes

            if (i == 0) begin : first_pe

                pe #(
                    .DATA_WIDTH(DATA_WIDTH)
                ) pe_inst (
                    .clk     (clk),
                    .compute (compute),
                    .init    (init),
                    .A       (input_a),
                    .B       (input_b[i]),
                    .X       (pe_outputs[i])
                );

            end
            else begin : other_pes

                pe #(
                    .DATA_WIDTH(DATA_WIDTH)
                ) pe_inst (
                    .clk     (clk),
                    .compute (compute),
                    .init    (init),
                    .A       (pe_outputs[i-1]),
                    .B       (input_b[i]),
                    .X       (pe_outputs[i])
                );

            end
        end
    endgenerate

    assign array_output = pe_outputs[NUM_PES-1];

endmodule