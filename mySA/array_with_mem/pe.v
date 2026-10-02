module pe #(
  parameter integer DATA_WIDTH = 10
) (
    input clk,
    input compute,
    input  logic unsigned [DATA_WIDTH-1:0] A,
    input  logic unsigned [DATA_WIDTH-1:0] B,
    output logic unsigned [DATA_WIDTH-1:0]   X,
    input init
);
    reg [(2*DATA_WIDTH)+1:0] state;

    always @ (posedge clk) 
        if (init)
            state <= 0;
        else
        if (compute)
            // temp = A * B;
            state <= (A*B);

    assign X = state[DATA_WIDTH-1:0];

endmodule