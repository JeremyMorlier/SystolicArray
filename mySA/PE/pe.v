module pe #(
  parameter integer DATA_WIDTH = 10
) (
    input clk,
    input compute,
    input  logic unsigned [DATA_WIDTH-1:0] A,
    input  logic unsigned [DATA_WIDTH-1:0] B,
    input  logic unsigned [DATA_WIDTH-1:0] C,
    output logic unsigned [(2*DATA_WIDTH)+1:0]   X
);
    reg [(2*DATA_WIDTH)+1:0] state;

    always @ (posedge clk) 
        if (compute)
            // temp = A * B;
            state <= (A * B) + ((2*DATA_WIDTH)+1)'(C);

    assign X = state;

endmodule