// Experimental simulation models for the five RAM configurations used by WasMetal.
// No delay or electrical model. The reference checks use unmodified Xilinx Unisim.
module wasmetal_xc7_ram #(
    parameter integer WIDTH=9, DATA_BITS=16384, PARITY_BITS=2048,
    parameter [DATA_BITS-1:0] INIT_DATA='0,
    parameter [PARITY_BITS-1:0] INIT_PARITY='0,
    parameter [63:0] OUTPUT_INIT_DATA=0, OUTPUT_RESET_DATA=0,
    parameter [7:0] OUTPUT_INIT_PARITY=0, OUTPUT_RESET_PARITY=0,
    parameter READ_FIRST=1
)(
    input wclk,rclk,wen,ren,rrst,
    input [14:0] waddr,raddr,
    input [63:0] wdata,
    input [7:0] wparity,wmask,
    output reg [63:0] rdata,
    output reg [7:0] rparity
);
    localparam integer LANES=WIDTH/9, DEPTH=DATA_BITS/(8*LANES);
    localparam integer SHIFT=$clog2(WIDTH)-1, ADDRESS_WIDTH=$clog2(DEPTH);
    wire [ADDRESS_WIDTH-1:0] write_index=waddr[SHIFT+:ADDRESS_WIDTH];
    wire [ADDRESS_WIDTH-1:0] read_index=raddr[SHIFT+:ADDRESS_WIDTH];
    reg [WIDTH-1:0] words[0:DEPTH-1];
    reg [WIDTH-1:0] q;
    initial begin
        for(integer word_index=0;word_index<DEPTH;word_index=word_index+1)
            for(integer lane=0;lane<LANES;lane=lane+1)
                words[word_index][lane*9+:9]=9'b0;
        for(integer lane=0;lane<LANES;lane=lane+1)
            q[lane*9+:9]={OUTPUT_INIT_PARITY[lane],OUTPUT_INIT_DATA[lane*8+:8]};
    end
    always @(posedge wclk)
        if(wen)
            for(integer lane=0;lane<LANES;lane=lane+1)
                if(wmask[lane])
                    words[write_index][lane*9+:9]<={
                        wparity[lane],wdata[lane*8+:8]};
    always @(posedge rclk)
        if(ren) begin
            if(rrst)
                for(integer lane=0;lane<LANES;lane=lane+1)
                    q[lane*9+:9]<={OUTPUT_RESET_PARITY[lane],OUTPUT_RESET_DATA[lane*8+:8]};
            else begin
                // WRITE_FIRST SDP in this model requires non-overlapping active
                // clock phases when the read/write addresses coincide.
                if(!READ_FIRST && wclk && wen && (|wmask) && write_index==read_index)
                    $fatal(1,"UNSUPPORTED_XC7_RAM_COLLISION");
                q<=words[read_index];
            end
        end
    always @* begin
        rdata='x; rparity='x;
        for(integer lane=0;lane<LANES;lane=lane+1) begin
            rdata[lane*8+:8]=q[lane*9+:8];
            rparity[lane]=q[lane*9+8];
        end
    end
endmodule

module RAMB18E1 #(
    parameter integer DOA_REG=0,DOB_REG=0,READ_WIDTH_A=0,READ_WIDTH_B=0,WRITE_WIDTH_A=0,WRITE_WIDTH_B=0,
    parameter RAM_MODE="TDP",WRITE_MODE_A="WRITE_FIRST",WRITE_MODE_B="WRITE_FIRST",
    parameter RSTREG_PRIORITY_A="RSTREG",RSTREG_PRIORITY_B="RSTREG",
    parameter RDADDR_COLLISION_HWCONFIG="DELAYED_WRITE",SIM_COLLISION_CHECK="ALL",SIM_DEVICE="7SERIES",INIT_FILE="NONE",
    parameter [17:0] INIT_A=0,INIT_B=0,SRVAL_A=0,SRVAL_B=0,
    parameter IS_CLKARDCLK_INVERTED=1'b0,
    parameter IS_CLKBWRCLK_INVERTED=1'b0,
    parameter IS_ENARDEN_INVERTED=1'b0,
    parameter IS_ENBWREN_INVERTED=1'b0,
    parameter IS_RSTRAMARSTRAM_INVERTED=1'b0,
    parameter IS_RSTRAMB_INVERTED=1'b0,
    parameter IS_RSTREGARSTREG_INVERTED=1'b0,
    parameter IS_RSTREGB_INVERTED=1'b0,
    parameter [255:0] INIT_00=0,
    parameter [255:0] INIT_01=0,
    parameter [255:0] INIT_02=0,
    parameter [255:0] INIT_03=0,
    parameter [255:0] INIT_04=0,
    parameter [255:0] INIT_05=0,
    parameter [255:0] INIT_06=0,
    parameter [255:0] INIT_07=0,
    parameter [255:0] INIT_08=0,
    parameter [255:0] INIT_09=0,
    parameter [255:0] INIT_0A=0,
    parameter [255:0] INIT_0B=0,
    parameter [255:0] INIT_0C=0,
    parameter [255:0] INIT_0D=0,
    parameter [255:0] INIT_0E=0,
    parameter [255:0] INIT_0F=0,
    parameter [255:0] INIT_10=0,
    parameter [255:0] INIT_11=0,
    parameter [255:0] INIT_12=0,
    parameter [255:0] INIT_13=0,
    parameter [255:0] INIT_14=0,
    parameter [255:0] INIT_15=0,
    parameter [255:0] INIT_16=0,
    parameter [255:0] INIT_17=0,
    parameter [255:0] INIT_18=0,
    parameter [255:0] INIT_19=0,
    parameter [255:0] INIT_1A=0,
    parameter [255:0] INIT_1B=0,
    parameter [255:0] INIT_1C=0,
    parameter [255:0] INIT_1D=0,
    parameter [255:0] INIT_1E=0,
    parameter [255:0] INIT_1F=0,
    parameter [255:0] INIT_20=0,
    parameter [255:0] INIT_21=0,
    parameter [255:0] INIT_22=0,
    parameter [255:0] INIT_23=0,
    parameter [255:0] INIT_24=0,
    parameter [255:0] INIT_25=0,
    parameter [255:0] INIT_26=0,
    parameter [255:0] INIT_27=0,
    parameter [255:0] INIT_28=0,
    parameter [255:0] INIT_29=0,
    parameter [255:0] INIT_2A=0,
    parameter [255:0] INIT_2B=0,
    parameter [255:0] INIT_2C=0,
    parameter [255:0] INIT_2D=0,
    parameter [255:0] INIT_2E=0,
    parameter [255:0] INIT_2F=0,
    parameter [255:0] INIT_30=0,
    parameter [255:0] INIT_31=0,
    parameter [255:0] INIT_32=0,
    parameter [255:0] INIT_33=0,
    parameter [255:0] INIT_34=0,
    parameter [255:0] INIT_35=0,
    parameter [255:0] INIT_36=0,
    parameter [255:0] INIT_37=0,
    parameter [255:0] INIT_38=0,
    parameter [255:0] INIT_39=0,
    parameter [255:0] INIT_3A=0,
    parameter [255:0] INIT_3B=0,
    parameter [255:0] INIT_3C=0,
    parameter [255:0] INIT_3D=0,
    parameter [255:0] INIT_3E=0,
    parameter [255:0] INIT_3F=0,
    parameter [255:0] INITP_00=0,
    parameter [255:0] INITP_01=0,
    parameter [255:0] INITP_02=0,
    parameter [255:0] INITP_03=0,
    parameter [255:0] INITP_04=0,
    parameter [255:0] INITP_05=0,
    parameter [255:0] INITP_06=0,
    parameter [255:0] INITP_07=0
)(
    output [15:0] DOADO,DOBDO,
    output [1:0] DOPADOP,DOPBDOP,
    input [13:0] ADDRARDADDR,ADDRBWRADDR,
    input CLKARDCLK,CLKBWRCLK,ENARDEN,ENBWREN,REGCEAREGCE,REGCEB,
    input RSTRAMARSTRAM,RSTRAMB,RSTREGARSTREG,RSTREGB,
    input [15:0] DIADI,DIBDI,
    input [1:0] DIPADIP,DIPBDIP,
    input [1:0] WEA,
    input [3:0] WEBWE
);
    localparam SDP=(RAM_MODE=="SDP");
    localparam integer WIDTH=SDP ? 36 : (READ_WIDTH_B==0 ? 9 : READ_WIDTH_B);
    localparam integer LANES=WIDTH/9;
    localparam VALID_TDP=(RAM_MODE=="TDP" && READ_WIDTH_A==0 && WRITE_WIDTH_B==0 &&
        WRITE_WIDTH_A==READ_WIDTH_B && READ_WIDTH_B==9 &&
        WRITE_MODE_A=="READ_FIRST" && WRITE_MODE_B=="READ_FIRST");
    localparam VALID_SDP=(SDP && READ_WIDTH_A==36 && READ_WIDTH_B==0 &&
        WRITE_WIDTH_A==0 && WRITE_WIDTH_B==36 &&
        WRITE_MODE_A=="WRITE_FIRST" && WRITE_MODE_B=="WRITE_FIRST");
    initial begin
        if((VALID_TDP || VALID_SDP)!==1'b1 ||
            DOA_REG!==0 || DOB_REG!==0 ||
            {IS_CLKARDCLK_INVERTED,IS_CLKBWRCLK_INVERTED,IS_ENARDEN_INVERTED,IS_ENBWREN_INVERTED,
             IS_RSTRAMARSTRAM_INVERTED,IS_RSTRAMB_INVERTED,IS_RSTREGARSTREG_INVERTED,IS_RSTREGB_INVERTED} !== 8'b0 ||
            INIT_FILE!="NONE" || SIM_DEVICE!="7SERIES" || SIM_COLLISION_CHECK!="ALL" ||
            RDADDR_COLLISION_HWCONFIG!="DELAYED_WRITE" ||
            RSTREG_PRIORITY_A!="RSTREG" || RSTREG_PRIORITY_B!="RSTREG")
            $fatal(1,"UNSUPPORTED_XC7_RAM_CONFIGURATION");
    end
    wire [63:0] data;
    wire [7:0] parity;
    wasmetal_xc7_ram #(
        .WIDTH(WIDTH),.DATA_BITS(16384),.PARITY_BITS(2048),
        .INIT_DATA({INIT_3F,INIT_3E,INIT_3D,INIT_3C,INIT_3B,INIT_3A,INIT_39,INIT_38,INIT_37,INIT_36,INIT_35,INIT_34,INIT_33,INIT_32,INIT_31,INIT_30,INIT_2F,INIT_2E,INIT_2D,INIT_2C,INIT_2B,INIT_2A,INIT_29,INIT_28,INIT_27,INIT_26,INIT_25,INIT_24,INIT_23,INIT_22,INIT_21,INIT_20,INIT_1F,INIT_1E,INIT_1D,INIT_1C,INIT_1B,INIT_1A,INIT_19,INIT_18,INIT_17,INIT_16,INIT_15,INIT_14,INIT_13,INIT_12,INIT_11,INIT_10,INIT_0F,INIT_0E,INIT_0D,INIT_0C,INIT_0B,INIT_0A,INIT_09,INIT_08,INIT_07,INIT_06,INIT_05,INIT_04,INIT_03,INIT_02,INIT_01,INIT_00}),
        .INIT_PARITY({INITP_07,INITP_06,INITP_05,INITP_04,INITP_03,INITP_02,INITP_01,INITP_00}),
        .OUTPUT_INIT_DATA(SDP ? {INIT_B[15:0],INIT_A[15:0]} : INIT_B),
        .OUTPUT_INIT_PARITY(SDP ? {INIT_B[17:16],INIT_A[17:16]} : INIT_B>>(8*LANES)),
        .OUTPUT_RESET_DATA(SDP ? {SRVAL_B[15:0],SRVAL_A[15:0]} : SRVAL_B),
        .OUTPUT_RESET_PARITY(SDP ? {SRVAL_B[17:16],SRVAL_A[17:16]} : SRVAL_B>>(8*LANES)),
        .READ_FIRST(!SDP)
    ) memory (
        .wclk(SDP ? CLKBWRCLK : CLKARDCLK),.rclk(SDP ? CLKARDCLK : CLKBWRCLK),
        .wen(SDP ? ENBWREN : ENARDEN),.ren(SDP ? ENARDEN : ENBWREN),
        .rrst(SDP ? RSTRAMARSTRAM : RSTRAMB),
        .waddr({1'b0,SDP ? ADDRBWRADDR : ADDRARDADDR}),
        .raddr({1'b0,SDP ? ADDRARDADDR : ADDRBWRADDR}),
        .wdata(SDP ? {DIBDI,DIADI} : DIADI),.wparity(SDP ? {DIPBDIP,DIPADIP} : DIPADIP),
        .wmask(SDP ? WEBWE : WEA),.rdata(data),.rparity(parity)
    );
    assign DOADO=SDP ? data[15:0] : 16'bx;
    assign DOPADOP=SDP ? parity[1:0] : 2'bx;
    assign DOBDO=SDP ? data[31:16] : data[15:0];
    assign DOPBDOP=SDP ? parity[3:2] : parity[1:0];
endmodule

module RAMB36E1 #(
    parameter integer DOA_REG=0,DOB_REG=0,READ_WIDTH_A=0,READ_WIDTH_B=0,WRITE_WIDTH_A=0,WRITE_WIDTH_B=0,
    parameter RAM_MODE="TDP",WRITE_MODE_A="WRITE_FIRST",WRITE_MODE_B="WRITE_FIRST",
    parameter RSTREG_PRIORITY_A="RSTREG",RSTREG_PRIORITY_B="RSTREG",
    parameter RDADDR_COLLISION_HWCONFIG="DELAYED_WRITE",SIM_COLLISION_CHECK="ALL",SIM_DEVICE="7SERIES",INIT_FILE="NONE",
    parameter [35:0] INIT_A=0,INIT_B=0,SRVAL_A=0,SRVAL_B=0,
    parameter IS_CLKARDCLK_INVERTED=1'b0,
    parameter IS_CLKBWRCLK_INVERTED=1'b0,
    parameter IS_ENARDEN_INVERTED=1'b0,
    parameter IS_ENBWREN_INVERTED=1'b0,
    parameter IS_RSTRAMARSTRAM_INVERTED=1'b0,
    parameter IS_RSTRAMB_INVERTED=1'b0,
    parameter IS_RSTREGARSTREG_INVERTED=1'b0,
    parameter IS_RSTREGB_INVERTED=1'b0,
    parameter RAM_EXTENSION_A="NONE",RAM_EXTENSION_B="NONE",EN_ECC_READ="FALSE",EN_ECC_WRITE="FALSE",
    parameter [255:0] INIT_00=0,
    parameter [255:0] INIT_01=0,
    parameter [255:0] INIT_02=0,
    parameter [255:0] INIT_03=0,
    parameter [255:0] INIT_04=0,
    parameter [255:0] INIT_05=0,
    parameter [255:0] INIT_06=0,
    parameter [255:0] INIT_07=0,
    parameter [255:0] INIT_08=0,
    parameter [255:0] INIT_09=0,
    parameter [255:0] INIT_0A=0,
    parameter [255:0] INIT_0B=0,
    parameter [255:0] INIT_0C=0,
    parameter [255:0] INIT_0D=0,
    parameter [255:0] INIT_0E=0,
    parameter [255:0] INIT_0F=0,
    parameter [255:0] INIT_10=0,
    parameter [255:0] INIT_11=0,
    parameter [255:0] INIT_12=0,
    parameter [255:0] INIT_13=0,
    parameter [255:0] INIT_14=0,
    parameter [255:0] INIT_15=0,
    parameter [255:0] INIT_16=0,
    parameter [255:0] INIT_17=0,
    parameter [255:0] INIT_18=0,
    parameter [255:0] INIT_19=0,
    parameter [255:0] INIT_1A=0,
    parameter [255:0] INIT_1B=0,
    parameter [255:0] INIT_1C=0,
    parameter [255:0] INIT_1D=0,
    parameter [255:0] INIT_1E=0,
    parameter [255:0] INIT_1F=0,
    parameter [255:0] INIT_20=0,
    parameter [255:0] INIT_21=0,
    parameter [255:0] INIT_22=0,
    parameter [255:0] INIT_23=0,
    parameter [255:0] INIT_24=0,
    parameter [255:0] INIT_25=0,
    parameter [255:0] INIT_26=0,
    parameter [255:0] INIT_27=0,
    parameter [255:0] INIT_28=0,
    parameter [255:0] INIT_29=0,
    parameter [255:0] INIT_2A=0,
    parameter [255:0] INIT_2B=0,
    parameter [255:0] INIT_2C=0,
    parameter [255:0] INIT_2D=0,
    parameter [255:0] INIT_2E=0,
    parameter [255:0] INIT_2F=0,
    parameter [255:0] INIT_30=0,
    parameter [255:0] INIT_31=0,
    parameter [255:0] INIT_32=0,
    parameter [255:0] INIT_33=0,
    parameter [255:0] INIT_34=0,
    parameter [255:0] INIT_35=0,
    parameter [255:0] INIT_36=0,
    parameter [255:0] INIT_37=0,
    parameter [255:0] INIT_38=0,
    parameter [255:0] INIT_39=0,
    parameter [255:0] INIT_3A=0,
    parameter [255:0] INIT_3B=0,
    parameter [255:0] INIT_3C=0,
    parameter [255:0] INIT_3D=0,
    parameter [255:0] INIT_3E=0,
    parameter [255:0] INIT_3F=0,
    parameter [255:0] INIT_40=0,
    parameter [255:0] INIT_41=0,
    parameter [255:0] INIT_42=0,
    parameter [255:0] INIT_43=0,
    parameter [255:0] INIT_44=0,
    parameter [255:0] INIT_45=0,
    parameter [255:0] INIT_46=0,
    parameter [255:0] INIT_47=0,
    parameter [255:0] INIT_48=0,
    parameter [255:0] INIT_49=0,
    parameter [255:0] INIT_4A=0,
    parameter [255:0] INIT_4B=0,
    parameter [255:0] INIT_4C=0,
    parameter [255:0] INIT_4D=0,
    parameter [255:0] INIT_4E=0,
    parameter [255:0] INIT_4F=0,
    parameter [255:0] INIT_50=0,
    parameter [255:0] INIT_51=0,
    parameter [255:0] INIT_52=0,
    parameter [255:0] INIT_53=0,
    parameter [255:0] INIT_54=0,
    parameter [255:0] INIT_55=0,
    parameter [255:0] INIT_56=0,
    parameter [255:0] INIT_57=0,
    parameter [255:0] INIT_58=0,
    parameter [255:0] INIT_59=0,
    parameter [255:0] INIT_5A=0,
    parameter [255:0] INIT_5B=0,
    parameter [255:0] INIT_5C=0,
    parameter [255:0] INIT_5D=0,
    parameter [255:0] INIT_5E=0,
    parameter [255:0] INIT_5F=0,
    parameter [255:0] INIT_60=0,
    parameter [255:0] INIT_61=0,
    parameter [255:0] INIT_62=0,
    parameter [255:0] INIT_63=0,
    parameter [255:0] INIT_64=0,
    parameter [255:0] INIT_65=0,
    parameter [255:0] INIT_66=0,
    parameter [255:0] INIT_67=0,
    parameter [255:0] INIT_68=0,
    parameter [255:0] INIT_69=0,
    parameter [255:0] INIT_6A=0,
    parameter [255:0] INIT_6B=0,
    parameter [255:0] INIT_6C=0,
    parameter [255:0] INIT_6D=0,
    parameter [255:0] INIT_6E=0,
    parameter [255:0] INIT_6F=0,
    parameter [255:0] INIT_70=0,
    parameter [255:0] INIT_71=0,
    parameter [255:0] INIT_72=0,
    parameter [255:0] INIT_73=0,
    parameter [255:0] INIT_74=0,
    parameter [255:0] INIT_75=0,
    parameter [255:0] INIT_76=0,
    parameter [255:0] INIT_77=0,
    parameter [255:0] INIT_78=0,
    parameter [255:0] INIT_79=0,
    parameter [255:0] INIT_7A=0,
    parameter [255:0] INIT_7B=0,
    parameter [255:0] INIT_7C=0,
    parameter [255:0] INIT_7D=0,
    parameter [255:0] INIT_7E=0,
    parameter [255:0] INIT_7F=0,
    parameter [255:0] INITP_00=0,
    parameter [255:0] INITP_01=0,
    parameter [255:0] INITP_02=0,
    parameter [255:0] INITP_03=0,
    parameter [255:0] INITP_04=0,
    parameter [255:0] INITP_05=0,
    parameter [255:0] INITP_06=0,
    parameter [255:0] INITP_07=0,
    parameter [255:0] INITP_08=0,
    parameter [255:0] INITP_09=0,
    parameter [255:0] INITP_0A=0,
    parameter [255:0] INITP_0B=0,
    parameter [255:0] INITP_0C=0,
    parameter [255:0] INITP_0D=0,
    parameter [255:0] INITP_0E=0,
    parameter [255:0] INITP_0F=0
)(
    output [31:0] DOADO,DOBDO,
    output [3:0] DOPADOP,DOPBDOP,
    input [15:0] ADDRARDADDR,ADDRBWRADDR,
    input CLKARDCLK,CLKBWRCLK,ENARDEN,ENBWREN,REGCEAREGCE,REGCEB,
    input RSTRAMARSTRAM,RSTRAMB,RSTREGARSTREG,RSTREGB,
    input [31:0] DIADI,DIBDI,
    input [3:0] DIPADIP,DIPBDIP,
    input [3:0] WEA,
    input [7:0] WEBWE,
    input CASCADEINA,CASCADEINB,INJECTDBITERR,INJECTSBITERR,
    output CASCADEOUTA,CASCADEOUTB,DBITERR,SBITERR,
    output [7:0] ECCPARITY,
    output [8:0] RDADDRECC
);
    localparam SDP=(RAM_MODE=="SDP");
    localparam integer WIDTH=SDP ? 72 : (READ_WIDTH_B==0 ? 9 : READ_WIDTH_B);
    localparam integer LANES=WIDTH/9;
    localparam VALID_TDP=(RAM_MODE=="TDP" && READ_WIDTH_A==0 && WRITE_WIDTH_B==0 &&
        WRITE_WIDTH_A==READ_WIDTH_B && (READ_WIDTH_B==18 || READ_WIDTH_B==36) &&
        WRITE_MODE_A=="READ_FIRST" && WRITE_MODE_B=="READ_FIRST");
    localparam VALID_SDP=(SDP && READ_WIDTH_A==72 && READ_WIDTH_B==0 &&
        WRITE_WIDTH_A==0 && WRITE_WIDTH_B==72 &&
        WRITE_MODE_A=="WRITE_FIRST" && WRITE_MODE_B=="WRITE_FIRST");
    initial begin
        if((VALID_TDP || VALID_SDP)!==1'b1 ||
            DOA_REG!==0 || DOB_REG!==0 ||
            {IS_CLKARDCLK_INVERTED,IS_CLKBWRCLK_INVERTED,IS_ENARDEN_INVERTED,IS_ENBWREN_INVERTED,
             IS_RSTRAMARSTRAM_INVERTED,IS_RSTRAMB_INVERTED,IS_RSTREGARSTREG_INVERTED,IS_RSTREGB_INVERTED} !== 8'b0 ||
            INIT_FILE!="NONE" || SIM_DEVICE!="7SERIES" || SIM_COLLISION_CHECK!="ALL" ||
            RDADDR_COLLISION_HWCONFIG!="DELAYED_WRITE" ||
            RSTREG_PRIORITY_A!="RSTREG" || RSTREG_PRIORITY_B!="RSTREG" ||
            RAM_EXTENSION_A!="NONE" || RAM_EXTENSION_B!="NONE" ||
            EN_ECC_READ!="FALSE" || EN_ECC_WRITE!="FALSE")
            $fatal(1,"UNSUPPORTED_XC7_RAM_CONFIGURATION");
    end
    wire [63:0] data;
    wire [7:0] parity;
    wasmetal_xc7_ram #(
        .WIDTH(WIDTH),.DATA_BITS(32768),.PARITY_BITS(4096),
        .INIT_DATA({INIT_7F,INIT_7E,INIT_7D,INIT_7C,INIT_7B,INIT_7A,INIT_79,INIT_78,INIT_77,INIT_76,INIT_75,INIT_74,INIT_73,INIT_72,INIT_71,INIT_70,INIT_6F,INIT_6E,INIT_6D,INIT_6C,INIT_6B,INIT_6A,INIT_69,INIT_68,INIT_67,INIT_66,INIT_65,INIT_64,INIT_63,INIT_62,INIT_61,INIT_60,INIT_5F,INIT_5E,INIT_5D,INIT_5C,INIT_5B,INIT_5A,INIT_59,INIT_58,INIT_57,INIT_56,INIT_55,INIT_54,INIT_53,INIT_52,INIT_51,INIT_50,INIT_4F,INIT_4E,INIT_4D,INIT_4C,INIT_4B,INIT_4A,INIT_49,INIT_48,INIT_47,INIT_46,INIT_45,INIT_44,INIT_43,INIT_42,INIT_41,INIT_40,INIT_3F,INIT_3E,INIT_3D,INIT_3C,INIT_3B,INIT_3A,INIT_39,INIT_38,INIT_37,INIT_36,INIT_35,INIT_34,INIT_33,INIT_32,INIT_31,INIT_30,INIT_2F,INIT_2E,INIT_2D,INIT_2C,INIT_2B,INIT_2A,INIT_29,INIT_28,INIT_27,INIT_26,INIT_25,INIT_24,INIT_23,INIT_22,INIT_21,INIT_20,INIT_1F,INIT_1E,INIT_1D,INIT_1C,INIT_1B,INIT_1A,INIT_19,INIT_18,INIT_17,INIT_16,INIT_15,INIT_14,INIT_13,INIT_12,INIT_11,INIT_10,INIT_0F,INIT_0E,INIT_0D,INIT_0C,INIT_0B,INIT_0A,INIT_09,INIT_08,INIT_07,INIT_06,INIT_05,INIT_04,INIT_03,INIT_02,INIT_01,INIT_00}),
        .INIT_PARITY({INITP_0F,INITP_0E,INITP_0D,INITP_0C,INITP_0B,INITP_0A,INITP_09,INITP_08,INITP_07,INITP_06,INITP_05,INITP_04,INITP_03,INITP_02,INITP_01,INITP_00}),
        .OUTPUT_INIT_DATA(SDP ? {INIT_B[31:0],INIT_A[31:0]} : INIT_B),
        .OUTPUT_INIT_PARITY(SDP ? {INIT_B[35:32],INIT_A[35:32]} : INIT_B>>(8*LANES)),
        .OUTPUT_RESET_DATA(SDP ? {SRVAL_B[31:0],SRVAL_A[31:0]} : SRVAL_B),
        .OUTPUT_RESET_PARITY(SDP ? {SRVAL_B[35:32],SRVAL_A[35:32]} : SRVAL_B>>(8*LANES)),
        .READ_FIRST(!SDP)
    ) memory (
        .wclk(SDP ? CLKBWRCLK : CLKARDCLK),.rclk(SDP ? CLKARDCLK : CLKBWRCLK),
        .wen(SDP ? ENBWREN : ENARDEN),.ren(SDP ? ENARDEN : ENBWREN),
        .rrst(SDP ? RSTRAMARSTRAM : RSTRAMB),
        .waddr((SDP ? ADDRBWRADDR[14:0] : ADDRARDADDR[14:0])),
        .raddr((SDP ? ADDRARDADDR[14:0] : ADDRBWRADDR[14:0])),
        .wdata(SDP ? {DIBDI,DIADI} : DIADI),.wparity(SDP ? {DIPBDIP,DIPADIP} : DIPADIP),
        .wmask(SDP ? WEBWE : WEA),.rdata(data),.rparity(parity)
    );
    assign DOADO=SDP ? data[31:0] : 32'bx;
    assign DOPADOP=SDP ? parity[3:0] : 4'bx;
    assign DOBDO=SDP ? data[63:32] : data[31:0];
    assign DOPBDOP=SDP ? parity[7:4] : parity[3:0];
    assign CASCADEOUTA=1'bx,CASCADEOUTB=1'bx,DBITERR=1'b0,SBITERR=1'b0;
    assign ECCPARITY=8'bx,RDADDRECC=9'bx;
endmodule
