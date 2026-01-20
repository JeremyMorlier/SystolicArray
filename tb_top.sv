module tb_top ();

    reg clk;
    reg reset;
    reg d;
    wire q;

    // Design Instantation
    d_ff dff_0 ( .clk(clk),
                .reset(reset),
                .d(d),
                .q(q));
    

    always #10 clk <= ~clk;
    
    initial begin
        $display("Hello World");
        reset = 0;
        d = 0;
        $display("[%0t]", $time, reset, q, d, clk);
        #10 reset = 1;
        $display("[%0t]", $time, reset, q, d, clk);
        #5 d = 1;
        $display("[%0t]", $time, reset, q, d, clk);
        #8 d = 0;
        $display("[%0t]", $time, reset, q, d, clk);
        #2 d = 1;
        $display("[%0t]", $time, reset, q, d, clk);
        #10 d = 0;
        $display("[%0t]", $time, reset, q, d, clk);


        $finish;

    end
endmodule
