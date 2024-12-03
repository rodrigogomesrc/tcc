#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <Arduino.h>

// Modelo convertido para C
const float pmdata_00[] PROGMEM = {-0.338005, -0.732521, 1.073688, };
const float pmdata_01[] PROGMEM = {0.968758, 0.293920, 0.287408, };
const float pmdata_02[] PROGMEM = {-0.710396, -0.273621, -0.419105, };
const float pmdata_03[] PROGMEM = {-1.489259, 1.104144, 0.352536, };
const float pmdata_04[] PROGMEM = {-0.685749, -0.892680, 0.217831, };
const float pmdata_05[] PROGMEM = {-0.665832, 0.413100, 1.372421, };
const float pmdata_06[] PROGMEM = {-0.488757, -0.187945, -0.289471, };
const float pmdata_07[] PROGMEM = {-0.303967, -0.081307, -0.157108, };
const float pmdata_08[] PROGMEM = {-0.000000, 0.000000, 0.000000, };
const float pmdata_09[] PROGMEM = {-0.277319, -0.125352, 0.920221, };
const float pmdata_10[] PROGMEM = {3.056480, 0.567247, -2.403121, 2.149412, -0.340662, -0.994181, -1.726729, -0.592236, -0.000000, -1.040911, };

int classifier(uint8_t * x){
    float result0[10];
    result0[0]=0;

    for(int i=0;i<3;i++){result0[0]+=(float)pgm_read_float_near(pmdata_00+i) * (float)x[i];}
    result0[1]=0;

    for(int i=0;i<3;i++){result0[1]+=(float)pgm_read_float_near(pmdata_01+i) * (float)x[i];}
    result0[2]=0;

    for(int i=0;i<3;i++){result0[2]+=(float)pgm_read_float_near(pmdata_02+i) * (float)x[i];}
    result0[3]=0;

    for(int i=0;i<3;i++){result0[3]+=(float)pgm_read_float_near(pmdata_03+i) * (float)x[i];}
    result0[4]=0;

    for(int i=0;i<3;i++){result0[4]+=(float)pgm_read_float_near(pmdata_04+i) * (float)x[i];}
    result0[5]=0;

    for(int i=0;i<3;i++){result0[5]+=(float)pgm_read_float_near(pmdata_05+i) * (float)x[i];}
    result0[6]=0;

    for(int i=0;i<3;i++){result0[6]+=(float)pgm_read_float_near(pmdata_06+i) * (float)x[i];}
    result0[7]=0;

    for(int i=0;i<3;i++){result0[7]+=(float)pgm_read_float_near(pmdata_07+i) * (float)x[i];}
    result0[8]=0;

    for(int i=0;i<3;i++){result0[8]+=(float)pgm_read_float_near(pmdata_08+i) * (float)x[i];}
    result0[9]=0;

    for(int i=0;i<3;i++){result0[9]+=(float)pgm_read_float_near(pmdata_09+i) * (float)x[i];}


    result0[0] = result0[0] + (-0.116790);
    result0[1] = result0[1] + (0.447825);
    result0[2] = result0[2] + (1.558155);
    result0[3] = result0[3] + (-0.343505);
    result0[4] = result0[4] + (-0.045461);
    result0[5] = result0[5] + (-0.294812);
    result0[6] = result0[6] + (1.057705);
    result0[7] = result0[7] + (0.560704);
    result0[8] = result0[8] + (-0.654517);
    result0[9] = result0[9] + (0.284379);

    for (int i=0; i < 10; i++){ if (result0[i] < 0) { result0[i] = 0;}}

    float result1[1];
    result1[0]=0;

    for(int i=0;i<10;i++){result1[0]+=(float)pgm_read_float_near(pmdata_10+i) * (float)result0[i];}
    result1[0] = result1[0] + (-0.109973);

    double max_el = result1[0];for (int i=1; i < 1; i++){max_el = max(max_el, result1[i]);}double exp_sum = 0.0; 

    for (int i=0; i<1; i++){ exp_sum += exp(result1[i]-max_el); } 

    for (int i=0; i<1; i++){ result1[i] = exp(result1[i]-max_el) / exp_sum; }

    int max_index = 0;

    for (int i = 0; i < 2; i++){ if (result1[i] > result1[max_index]){ max_index = i; }}
    
    return max_index;

}; 

//Fim do modelo

// Função para converter float para uint8_t
void convert_float_to_uint8(float *input, uint8_t *output, int length) {
    for (int i = 0; i < length; i++) {
        // Cast simples, truncando valores para o intervalo do modelo
        output[i] = (uint8_t)input[i];
    }
}

unsigned long previousMillis = 0;  // Armazena o tempo do último evento
const long interval = 5000;         // Intervalo de 5 segundos (5000 milissegundos)

void setup() {
    // Inicializa a comunicação serial
    Serial.begin(115200);
}

void loop() {
    unsigned long currentMillis = millis();  // Pega o tempo atual

    // Verifica se já se passaram 5 segundos
    if (currentMillis - previousMillis >= interval) {
        // Salva o tempo atual
        previousMillis = currentMillis;

        // Exemplos de entrada com floats
        float examples[3][3] = {
            {9.08, 13.53, 3.44},  // True
            {13.39, 12.11, 12.24}, // False
            {8.70, 3.83, 7.45}   // True
        };

        // Buffer para os valores convertidos
        uint8_t input_buffer[3];

        // Itera pelos exemplos, converte e classifica
        for (int i = 0; i < 3; i++) {
            // Converte as entradas float para uint8_t
            convert_float_to_uint8(examples[i], input_buffer, 3);

            // Classifica usando o modelo
            int result = classifier(input_buffer);

            // Mostra o resultado no monitor serial
            Serial.print("Exemplo ");
            Serial.print(i + 1);
            Serial.print(": Entrada = [");
            Serial.print(examples[i][0]);
            Serial.print(", ");
            Serial.print(examples[i][1]);
            Serial.print(", ");
            Serial.print(examples[i][2]);
            Serial.print("], Classe = ");
            Serial.println(result ? "True" : "False");
        }
    }
}