// SystemSimulation.cpp : Defines the entry point for the console application.
//

//#define DEBUG

// Must include controller.h
#include "controller.h"

//#include <random.h>
//#include <tchar>
//#include <iostream>
#ifdef DEBUG
  #include<stdio.h>
#endif

//#include <math.h>

//using namespace std;

#define N (100)

double SINE4[] = { 0.,  1.,  0., -1};

double SINE12[] = { 0.       ,  0.5      ,  0.8660254,  1.       ,  0.8660254,
        0.5      ,  0.       , -0.5      , -0.8660254, -1.       ,
       -0.8660254, -0.5      };

double SINE24[] = { 0.        ,  0.25881905,  0.5       ,  0.70710678,  0.8660254 ,
        0.96592583,  1.        ,  0.96592583,  0.8660254 ,  0.70710678,
        0.5       ,  0.25881905,  0.        , -0.25881905, -0.5       ,
       -0.70710678, -0.8660254 , -0.96592583, -1.        , -0.96592583,
       -0.8660254 , -0.70710678, -0.5       , -0.25881905};

double SINE50[] =
      { 0.        ,  0.12533323,  0.24868989,  0.36812455,  0.48175367,
        0.58778525,  0.68454711,  0.77051324,  0.84432793,  0.90482705,
        0.95105652,  0.98228725,  0.99802673,  0.99802673,  0.98228725,
        0.95105652,  0.90482705,  0.84432793,  0.77051324,  0.68454711,
        0.58778525,  0.48175367,  0.36812455,  0.24868989,  0.12533323,
       -0.        , -0.12533323, -0.24868989, -0.36812455, -0.48175367,
       -0.58778525, -0.68454711, -0.77051324, -0.84432793, -0.90482705,
       -0.95105652, -0.98228725, -0.99802673, -0.99802673, -0.98228725,
       -0.95105652, -0.90482705, -0.84432793, -0.77051324, -0.68454711,
       -0.58778525, -0.48175367, -0.36812455, -0.24868989, -0.12533323};

double SINE100[100] =
       {0.        ,  0.06279052,  0.12533323,  0.18738131,  0.24868989,
        0.30901699,  0.36812455,  0.42577929,  0.48175367,  0.53582679,
        0.58778525,  0.63742399,  0.68454711,  0.72896863,  0.77051324,
        0.80901699,  0.84432793,  0.87630668,  0.90482705,  0.92977649,
        0.95105652,  0.96858316,  0.98228725,  0.9921147 ,  0.99802673,
        1.        ,  0.99802673,  0.9921147 ,  0.98228725,  0.96858316,
        0.95105652,  0.92977649,  0.90482705,  0.87630668,  0.84432793,
        0.80901699,  0.77051324,  0.72896863,  0.68454711,  0.63742399,
        0.58778525,  0.53582679,  0.48175367,  0.42577929,  0.36812455,
        0.30901699,  0.24868989,  0.18738131,  0.12533323,  0.06279052,
       -0.        , -0.06279052, -0.12533323, -0.18738131, -0.24868989,
       -0.30901699, -0.36812455, -0.42577929, -0.48175367, -0.53582679,
       -0.58778525, -0.63742399, -0.68454711, -0.72896863, -0.77051324,
       -0.80901699, -0.84432793, -0.87630668, -0.90482705, -0.92977649,
       -0.95105652, -0.96858316, -0.98228725, -0.9921147 , -0.99802673,
       -1.        , -0.99802673, -0.9921147 , -0.98228725, -0.96858316,
       -0.95105652, -0.92977649, -0.90482705, -0.87630668, -0.84432793,
       -0.80901699, -0.77051324, -0.72896863, -0.68454711, -0.63742399,
       -0.58778525, -0.53582679, -0.48175367, -0.42577929, -0.36812455,
       -0.30901699, -0.24868989, -0.18738131, -0.12533323, -0.06279052};

#define PERIOD (500)
double get_tri(int n)
{
    double ret_val = 0;
    double offset = 1;

    if(n<=PERIOD/2) ret_val = n/10.;
    else ret_val = (PERIOD-n)/10.;
    return ret_val + offset;
}

double get_line(int n)
{
    return n;
}

double get_sin4(int n)
{
    double y;
    n = n % N;

    if(n==0) y = SINE4[0];
    else if(n==1) y = SINE4[1];
    else if(n==2) y = SINE4[2];
    else if(n==3) y = SINE4[3];
    else
    {
        //printf("Unexpected error!:%d\n",n);
        y = 0;
    }
    return y;
}
double get_sin(int n)
{
    double y;
    //n = n % N;

    if(n==0) y = SINE100[0];
    else if(n==1) y = SINE100[1];
    else if(n==2) y = SINE100[2];
    else if(n==3) y = SINE100[3];
    else if(n==4) y = SINE100[4];
    else if(n==5) y = SINE100[5];
    else if(n==6) y = SINE100[6];
    else if(n==7) y = SINE100[7];
    else if(n==8) y = SINE100[8];
    else if(n==9) y = SINE100[9];
    else if(n==10) y = SINE100[10];
    else if(n==11) y = SINE100[11];
    else if(n==12) y = SINE100[12];
    else if(n==13) y = SINE100[13];
    else if(n==14) y = SINE100[14];
    else if(n==15) y = SINE100[15];
    else if(n==16) y = SINE100[16];
    else if(n==17) y = SINE100[17];
    else if(n==18) y = SINE100[18];
    else if(n==19) y = SINE100[19];
    else if(n==20) y = SINE100[20];
    else if(n==21) y = SINE100[21];
    else if(n==22) y = SINE100[22];
    else if(n==23) y = SINE100[23];
    else if(n==24) y = SINE100[24];
    else if(n==25) y = SINE100[25];
    else if(n==26) y = SINE100[26];
    else if(n==27) y = SINE100[27];
    else if(n==28) y = SINE100[28];
    else if(n==29) y = SINE100[29];
    else if(n==30) y = SINE100[30];
    else if(n==31) y = SINE100[31];
    else if(n==32) y = SINE100[32];
    else if(n==33) y = SINE100[33];
    else if(n==34) y = SINE100[34];
    else if(n==35) y = SINE100[35];
    else if(n==36) y = SINE100[36];
    else if(n==37) y = SINE100[37];
    else if(n==38) y = SINE100[38];
    else if(n==39) y = SINE100[39];
    else if(n==40) y = SINE100[40];
    else if(n==41) y = SINE100[41];
    else if(n==42) y = SINE100[42];
    else if(n==43) y = SINE100[43];
    else if(n==44) y = SINE100[44];
    else if(n==45) y = SINE100[45];
    else if(n==46) y = SINE100[46];
    else if(n==47) y = SINE100[47];
    else if(n==48) y = SINE100[48];
    else if(n==49) y = SINE100[49];
    else if(n==50) y = SINE100[50];
    else if(n==51) y = SINE100[51];
    else if(n==52) y = SINE100[52];
    else if(n==53) y = SINE100[53];
    else if(n==54) y = SINE100[54];
    else if(n==55) y = SINE100[55];
    else if(n==56) y = SINE100[56];
    else if(n==57) y = SINE100[57];
    else if(n==58) y = SINE100[58];
    else if(n==59) y = SINE100[59];
    else if(n==60) y = SINE100[60];
    else if(n==61) y = SINE100[61];
    else if(n==62) y = SINE100[62];
    else if(n==63) y = SINE100[63];
    else if(n==64) y = SINE100[64];
    else if(n==65) y = SINE100[65];
    else if(n==66) y = SINE100[66];
    else if(n==67) y = SINE100[67];
    else if(n==68) y = SINE100[68];
    else if(n==69) y = SINE100[69];
    else if(n==70) y = SINE100[70];
    else if(n==71) y = SINE100[71];
    else if(n==72) y = SINE100[72];
    else if(n==73) y = SINE100[73];
    else if(n==74) y = SINE100[74];
    else if(n==75) y = SINE100[75];
    else if(n==76) y = SINE100[76];
    else if(n==77) y = SINE100[77];
    else if(n==78) y = SINE100[78];
    else if(n==79) y = SINE100[79];
    else if(n==80) y = SINE100[80];
    else if(n==81) y = SINE100[81];
    else if(n==82) y = SINE100[82];
    else if(n==83) y = SINE100[83];
    else if(n==84) y = SINE100[84];
    else if(n==85) y = SINE100[85];
    else if(n==86) y = SINE100[86];
    else if(n==87) y = SINE100[87];
    else if(n==88) y = SINE100[88];
    else if(n==89) y = SINE100[89];
    else if(n==90) y = SINE100[90];
    else if(n==91) y = SINE100[91];
    else if(n==92) y = SINE100[92];
    else if(n==93) y = SINE100[93];
    else if(n==94) y = SINE100[94];
    else if(n==95) y = SINE100[95];
    else if(n==96) y = SINE100[96];
    else if(n==97) y = SINE100[97];
    else if(n==98) y = SINE100[98];
    else if(n==99) y = SINE100[99];
    else
    {
        //printf("Unexpected error!\n");
        y = 0;
    }
    return y;
}


int myabs(double x){
    if(x>0.0)
        return x;
    else
        return -x;
}

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
    //double x_hat_m1_1, double x_hat_m1_2, double u_m1, double ref_1, double ref_2, double y_1, double y_2, double attk_1, double attk_2, double w_1, double w_2)
{
	/*
	Inputs:
		_i subscript denotes i-th element of the input vectors...
		x_hat_m1: Previous estimated value of the system states
		u_m1: Previous control inputs provided by this function
		ref: Reference signal for the controller
		y: output of the plant - recorded sensor values
		attk: Inpust of the attacker, to be added to sensor values
		w: sensor noise, to be added to sensor values
	Outputs:
		DetectorTriggered: boolean value, 0-no attack detected, 1-attack detected
		DetectorValue: Value that describes how close to the detection threshold is the input of the detector
		ControlSignal: Control signal to be provided to plant as inputs
		EstimatedStates: States estimated by the estimator
	Note:
		We are assuming matrix C of the system dynamics is I, to simplify computation. If not the case, residue computation needs to be changed
	*/

        double ref_1, ref_2, y1, y2;
        double w1, w2;
        double y1_noisy, y2_noisy;
        //clk
        unsigned int n;
	//Threshold triggering level
	const double threshold = 20;
	//Matrix A of the system dynamics
	const double a11 = 1; const double a12 = 0.01;
	const double a21 = 0; const double a22 = 1;
	//Matrix B of the system dynamics
	const double b11 = 0.0001;
	const double b21 = 0.01;
	//Matrix L of the LQR controller
	const double l11 = -0.9914; const double l12 = -1.7221;
        double ids = 0;

	double res_1=0, res_2=0;
        double u;

        y1 = input->x_arr[0];
        y2 = input->x_arr[1];

        n = input->int_state_arr[0];

        ref_1 = 10*get_tri(n);
        //ref_2 = 0;//1*get_tri(n);
        //ref_1 = 100*get_sin(n);
        //ref_1 = 1000*SINE100[n%N];
        ref_2 = 0;//100*get_sin(n+N/4);
        //printf("ref1: %f, ref2: %f\n", ref_1, ref_2);

        //ref_1 = 10;//*get_line(n);
        //ref_2 = -0;

        w1 = input->input_arr[0];
        w2 = input->input_arr[1];

        y1_noisy = y1 + w1;
        y2_noisy = y2 + w2;

	//Compute controller output
	u = l11*(y1_noisy - ref_1) + l12*(y2_noisy - ref_2);
        ret_val->output_arr[0] = u;

        ids = threshold - (myabs(w1) + myabs(w2));

//         if(ids>=0)
//             ret_val->output_arr[2] = 0;
//         else
//             ret_val->output_arr[2] = 1;
        ret_val->output_arr[2] = 1;

        //ret_val->output_arr[1] = (myabs(res_1) + myabs(res_2))>threshold;

        //printf("%f\n", ret_val->output_arr[1]);
        ret_val->output_arr[1] = ids;

        if(n>PERIOD) ret_val->int_state_arr[0] = 0;
        else ret_val->int_state_arr[0] = n + 1;

        ret_val->output_arr[3] = ref_1;
	return (void*)0;
}

int main(){}

#if 0

PlantOutputs SimulatePlant(double u,double x_m1_1,double x_m1_2, double w_1,double w_2)
{
	/*
	Inputs:
		u: Control inputs to the plant
		x_m1_1: Previous system state vector, first element
		x_m1_2: Previous system state vector, second element
		w_1: Random noise to be added on first system state
		w_2: Random noise to be added on second system state
	Outputs:
		SensorValues_1: sensor values generated by the plant, first vector element
		SensorValues_2: sensor values generated by the plant, second vector element
		SystemState_1: first vector element of the states of the system, required to generate next system state
		SystemState_2: second vector element of the states of the system, required to generate next system state
	Note:
		We are assuming matrix C of the system dynamics is I, to simplify computation. If not the case, output generation needs to be changed
	*/
	PlantOutputs GatherOutputs;

	//Matrix A of the system dynamics
	const double a11 = 1; const double a12 = 0.01;
	const double a21 = 0; const double a22 = 1;
	//Matrix B of the system dynamics
	const double b11 = 0.0001;
	const double b21 = 0.01;
	//Update system states
	double x_1 = (a11*x_m1_1 + a12*x_m1_2) + (b11*u);
	double x_2 = (a21*x_m1_1 + a22*x_m1_2) + (b21*u);
	//Compute system outputs - looks like this due to C==I
	double y_1 = x_1;
	double y_2 = x_2;

	GatherOutputs.SensorValues_1 = y_1;
	GatherOutputs.SensorValues_2 = y_2;
	GatherOutputs.SystemState_1 = x_1;
	GatherOutputs.SystemState_2 = x_2;

	return GatherOutputs;
}

int main()
{
	//initialize files for write/read
        //
	//ofstream OutFile;
	//OutFile.open("RecordedOuts.txt");

#ifdef DEBUG
        FILE* fp;
        fp = fopen("RecordedOuts.txt", "w");
	printf("Starting the code\n");
#endif

	//default_random_engine generator;
	//random_device generator;
	//normal_distribution<double> randn(0.0, 1.0);

	//initialize starting values
	double x_m1_1 = 0;
	double x_m1_2 = 0;
	double x_hat_m1_1 = 0;
	double x_hat_m1_2 = 0;
	double u = 0;
	double u_m1 = 0;
	int SimulationLength = 20000;
	ProcessorOutputs ProcOuts;
	PlantOutputs PlantOuts;
	for (int i = 0; i < SimulationLength; i++)
	{
		double w_x_1 = 1;//randn(generator);
		double w_x_2 = 1;//randn(generator);

		PlantOuts = SimulatePlant(u, x_m1_1, x_m1_2, w_x_1, w_x_2);
		x_m1_1 = PlantOuts.SystemState_1;
		x_m1_2 = PlantOuts.SystemState_2;

		//OutFile << x_m1_1 << ' ' << x_m1_2 << '\n';
                fprintf(fp, "%f %f\n", x_m1_1, x_m1_2);

		float y_1 = PlantOuts.SensorValues_1;
		float y_2 = PlantOuts.SensorValues_2;
		double w_y_1 = 1;//randn(generator);
		double w_y_2 = 1;//randn(generator);
		ProcOuts = controller(x_hat_m1_1, x_hat_m1_2, u_m1, 0, 0, y_1, y_2, 0, 0, w_y_1, w_y_2);
		u_m1 = u;
		x_hat_m1_1 = ProcOuts.EstimatedStates_1;
		x_hat_m1_2 = ProcOuts.EstimatedStates_2;
		u = ProcOuts.ControlSignal;
	}

	//for (int i = 0; i < 10000; i++)
	//{
	//	OutFile << randn(generator) << '\n';
	//}
	//cout << randn(generator) << ' ' << randn(generator) << ' ' << randn(generator) << '\n';
	//cout << ProcOuts.ControlSignal << ' ' << ProcOuts.DetectorTriggered << ' ' << ProcOuts.DetectorValue << '\n';

	//OutFile.close();
#ifdef DEBUG
        fclose(fp);
#endif
//system("PAUSE");
    return 0;
}
#endif
