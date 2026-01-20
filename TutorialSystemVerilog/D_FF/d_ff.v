module d_ff (clk, reset, q, d);

    input clk;
    input reset;
    input d;
    output q;

    reg q;

    always @ (posedge clk) 
        if (! reset)
            q <= 0;
        else
            q <= d;
    
endmodule
