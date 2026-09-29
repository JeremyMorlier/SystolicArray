module array #(
    parameter integer NUM_PES = 4,
    parameter integer DATA_WIDTH = 10
)(
    input  logic clk,
    input  logic compute,
    input  logic init,

    input  logic unsigned [DATA_WIDTH-1:0] input_a,
    input  logic unsigned [DATA_WIDTH-1:0] input_b [NUM_PES-1:0],

    output logic unsigned [DATA_WIDTH-1:0] array_output
);

    logic unsigned [DATA_WIDTH-1:0] pe_outputs [NUM_PES-1:0];

    genvar i;

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