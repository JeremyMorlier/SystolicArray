module adder #(
  parameter integer DATA_WIDTH = 10
) (
    input clk,
    input compute,
    input  logic unsigned [DATA_WIDTH-1:0] A,
    input  logic unsigned [DATA_WIDTH-1:0] B,
    output logic unsigned [DATA_WIDTH:0]   X
);
    reg [DATA_WIDTH:0] q;

    always @ (posedge clk) 
        if (compute)
            q = A + B;
        else
            q = 0;
    
    assign X = q;

endmodule