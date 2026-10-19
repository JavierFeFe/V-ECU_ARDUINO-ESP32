# Manuales y documentos consultados

Los PDF **no se incluyen en el repositorio** (son documentación de Volvo CE, Volvo Trucks, Volvo Penta, Deutz y de fabricantes de controladores, en muchos casos re-alojada por terceros). Esta tabla indica qué se consultó y dónde está cada archivo en la copia de trabajo local; las URL de origen, el contenido y la fiabilidad de cada documento están en las secciones **"Manuales descargables"** de los anexos [D](../anexos/D_familia_LucasVarity_D12.md), [E](../anexos/E_volvo_penta_deutz_emr2.md), [F](../anexos/F_L90E_L120E_misma_EECU.md) y [H](../anexos/H_deutz_emr2.md).

Documentos más importantes para el proyecto:

- **Volvo CE — UPDATE EC160B~460B** (`volvo_trucks_d12/Volvo_EC160B-EC460B_Service_Manual.pdf`, 31 p.): circuitos OEM de V-ECU y E-ECU, selector Auto/Manual, Resistor Box, interruptor de emergencia, códigos. Páginas renderizadas en `../esquemas/ce_EC-B_UPDATE_*` y `d12_EC-B_series_*`.
- **Volvo Trucks — Vectro II PV776-144528** (250 p.): pinouts EA/EB de la EECU D12 (misma familia de hardware), VECU, red J1939/J1587.
- **Volvo CE — Manual del operador EC210B (ser. 14132-)**: modos, interruptores 25/26, fusibles, tabla de corrientes.
- **Volvo CE — Esquemas L120E Sch01–Sch100**: misma E-ECU; conector EB, terminador R702 en el I-ECU, colores de cable.
- **Volvo Penta — Electrical Interface Specification EMS 47706587**: TSC1, VP70, direcciones de origen, mensajes del motor.
- **Deutz — EMR2 System Description 0297 9885**: pines F/M, consignas, limp-home, CAN.

## `volvo_ce/`

| Archivo | Páginas | Tamaño |
|---|---|---|
| Volvo_EC210B_Brochure_D6D_EAE2_2002-09.pdf | 12 | 564K |
| Volvo_EC210B_LC_Service_Manual_SamplePages_aservicemanualpdf.pdf | 39 | 1.3M |
| Volvo_EC210B_Operators_Manual_ser14132.pdf | 244 | 6.0M |
| Volvo_L120E_Service_Training_Electrical_Schematics_Sch01-Sch100.pdf | 38 | 956K |
| Volvo_L90E_Brochure_2005.pdf | 16 | 736K |

## `volvo_trucks_d12/`

| Archivo | Páginas | Tamaño |
|---|---|---|
| Eaton_TRIG0910_Volvo_Mack_BBM_Engine_Config.pdf | 32 | 412K |
| Volvo_A35D_A40D_Manual.pdf | 8 | 460K |
| Volvo_CE_EC210B_Spec_Sheet_2004.pdf | 12 | 412K |
| Volvo_D12A_Fault_Codes.pdf | 40 | 1.0M |
| Volvo_D12_D12A_D12B_D12C_Service_Manual.pdf | 48 | 672K |
| Volvo_D12_D12A_D12B_Engines_Workshop_Manual.pdf | 709 | 18M |
| Volvo_D7_D12_Engines_Service_Manual.pdf | 214 | 1.4M |
| Volvo_EC160B-EC460B_Service_Manual.pdf | 31 | 12M |
| Volvo_EC210B_Operators_Manual_sn14132-.pdf | 244 | 6.0M |
| Volvo_FH12_D12A_Fault_Codes_truckmanualshub.pdf | 4 | 360K |
| Volvo_FH12_FH16_Electrical_Wiring_Diagrams_Service_Manual.pdf | 128 | 3.7M |
| Volvo_FH12_FH16_RHD_Wiring_Diagrams.pdf | 114 | 3.2M |
| Volvo_J1939_J1708_Datalink_Fault_Tracing.pdf | 25 | 732K |
| Volvo_L120E_Electrical_Schematic_Diagram.pdf | 38 | 828K |
| Volvo_MID128_EECU_Fault_Code_Guide.pdf | 20 | 220K |
| Volvo_MID144_VECU_Codigos_Error_ES.pdf | 174 | 1.1M |
| Volvo_Penta_Marine_EMS_OpenCAN_Install_Guideline.pdf | 36 | 1.3M |
| Volvo_Penta_TAD1240-1242GE_EDCIII_Operators_Manual.pdf | 76 | 2.8M |
| Volvo_Reman_Technical_Application_Guide.pdf | 49 | 1.3M |
| Volvo_TSB_DataLink_Diagnostics_NHTSA_MC-10125875.pdf | 6 | 284K |
| Volvo_TSB_J1939_SourceAddress_NHTSA_MC-10141869.pdf | 394 | 1.2M |
| Volvo_TSI_Vectro_II_Vehicle_Management_System_PV776-144528.pdf | 250 | 4.5M |
| Volvo_Trucks_Electric_Wiring_Diagrams_jimcontent.pdf | 147 | 7.4M |
| Volvo_VHD2_VN_VT_Service_Manual.pdf | 130 | 328K |
| Volvo_VN_VHD_V2_Electrical_Schematic_PV776-20040447_2004-12.pdf | 208 | 4.9M |
| Volvo_VN_VHD_V2_VT_MID128_Fault_Code_Guide.pdf | 54 | 156K |
| Volvo_VN_VHD_VT_V2_Electrical_Schematic_PV776-20175317_2005-06.pdf | 128 | 2.9M |
| Volvo_VTC_BodyBuilder_PTO_Options_Europe.pdf | 50 | 3.5M |
| Volvo_VTNA_BodyBuilder_Sec3_Electrical_VECU4_2023.pdf | 166 | 8.5M |
| Volvo_VTNA_BodyBuilder_Sec9_PTO_VEC4_2023.pdf | 124 | 7.4M |

## `volvo_penta_tad/`

| Archivo | Páginas | Tamaño |
|---|---|---|
| Cattron_Dynagen_TOUGH_J1939_Reference_Manual.pdf | 43 | 888K |
| ComAp_ECU_List_7-0-0_Global_Guide_r3.pdf | 419 | 4.9M |
| ComAp_Electronic_Engines_Support_2015.pdf | 254 | 6.6M |
| VolvoPenta_Marine_D9_D13_D16_EMS_Electrical_Interface_Specification_47706587.pdf | 36 | 1.3M |
| VolvoPenta_TAD1241GE_Datasheet_EDCIII.pdf | 2 | 332K |
| VolvoPenta_TAD1641GE_Datasheet.pdf | 2 | 280K |
| VolvoPenta_TAD734GE_Datasheet_47709301.pdf | 2 | 368K |
| VolvoPenta_TAD734GE_TAD650-760VE_Group30_Electrical_Workshop_Manual_7747632_DEMO.pdf | 15 | 424K |
| VolvoPenta_TAD941GE_Datasheet_2p.pdf | 2 | 356K |
| VolvoPenta_TAD941GE_Datasheet_plus_OperatorsManual_9L_EMS2.pdf | 63 | 3.6M |
| YachtDevices_YDEG-04_Manual_J1939_VolvoPenta.pdf | 57 | 1.7M |

## `deutz_emr2/`

| Archivo | Páginas | Tamaño |
|---|---|---|
| ComAp_Electronic_Engines_Support_08-2015_r2.pdf | 254 | 6.6M |
| ComAp_Electronic_Engines_Support_7-0-0_Global_Guide_r3_2019.pdf | 419 | 4.9M |
| DEIF_AGC-4_MkII_Option_H12_H13_engine_communication_4189341274J.pdf | 233 | 2.3M |
| DEIF_AGC150_CAN_bus_engine_communication_4189341302I.pdf | 221 | 1.7M |
| DEIF_Omni_Engine_Interface_Communication_4189341306.pdf | 161 | 1.5M |
| Deutz_EMR2_System_Description_0297_9885_EN_06-2002_60p_idoc-tips.pdf | 60 | 1.4M |
| Deutz_EMR2_Systembeschreibung_traduction_FR_p59-118_futura-sciences.pdf | 60 | 828K |
| VolvoPenta_4-7L_EDC4_Operators_Manual_7745202_TAD722GE.pdf | 58 | 1.7M |
| Woodward_easYgen-1600_Technical_Manual_B37699A.pdf | 113 | 9.3M |
| Woodward_easYgen_Rental_Genset_ProductSpec_37553D_ECU_list.pdf | 4 | 892K |

