module pe #(
  parameter integer DATA_WIDTH = 10
) (
    input clk,
    input compute,
    input  logic unsigned [DATA_WIDTH-1:0] north,
    input  logic unsigned [DATA_WIDTH-1:0] west,
    output logic unsigned [DATA_WIDTH-1:0] east,
    output  logic unsigned [DATA_WIDTH-1:0] south,
    input init
);
    reg [(2*DATA_WIDTH)+1:0] state;

    always @ (posedge clk) 
        if (init)
            state <= 0;
        else
        if (compute)
            // MAC: state = state + north * west;
            state <= state + (north*west);

    assign east = state[DATA_WIDTH-1:0];
    assign south = north;

endmodule