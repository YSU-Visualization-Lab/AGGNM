<template>
  <div class="com-container">
    <div class="com-header" style="text-align: center; width:100%;">
      <h2 class="title">AGGNM: AGGNM based multi-scale pocket analysis allosteric pocket prediction method</h2>
      <div class="title-right">
      </div>
    </div>
    <div class="com-body">
      <!-- 导航栏 -->
      <div class="com-navig">
        <div  style="background-color:#A8A8A8; font-size: 14px; text-align:center"> <b>Protein Name</b></div>
        <br>
        <!-- 1 口袋编号 -->
        <b>PDB Entry: </b>
        <input type="text" name="firstname" v-model="pdbName" style="font-size: 10px; text-align:center; width: 90px;">
        <br>
        <br>
        <!-- 2 口袋相关信息 -->
        <div  style="background-color:#A8A8A8; font-size: 14px; text-align:center"> <b>Protein Info</b></div>
        <p style="font-size: 12px;text-align: left; margin-left: 5px; margin-right: 5px; margin-bottom: 10px;">
          <strong>PDB UniProt ID: </strong>
          <br>
          <p style="text-align: center;font-size: 12px;margin-left: 5px; margin-right: 5px;">
            {{ this.pdb_info_ls[ this.$store.state.pdbName ].UniProt }}
          </p>
        </p>
        <p style="font-size: 12px;text-align: left; margin-left: 5px; margin-right: 5px; margin-bottom: 10px;">
          <strong>PDB Classification: </strong>
          <br>
          <p style="text-align: center;font-size: 12px;margin-left: 5px; margin-right: 5px;">
            {{ this.pdb_info_ls[ this.$store.state.pdbName ].Classification }}
          </p>
        </p>
        <p style="font-size: 12px;text-align: left; margin-left: 5px; margin-right: 5px; margin-bottom: 10px;">
          <strong>PDB Organism: </strong>
          <br>
          <p style="text-align: center;font-size: 12px;margin-left: 5px; margin-right: 5px;">
            {{ this.pdb_info_ls[ this.$store.state.pdbName ].Organism }}
          </p>
        </p>
        <p style="background-color:#A8A8A8; font-size: 14px; text-align:center"><b>Protein Function</b> </p>
        <p style="font-size: 12px;text-align: left; margin-left: 5px; margin-right: 5px; margin-bottom: 10px;">
          <strong>PDB Organism: </strong>
          <br>
          <p style="text-align: center;font-size: 12px;margin-left: 5px; margin-right: 5px;">
            {{ this.pdb_info_ls[ this.$store.state.pdbName ].info }}
          </p>
        </p>
      </div>
      <!-- 视图左 -->
      <div class="body-left">
        <div id="left-top">
          <can1 v-if="has_data" :key="can1_key"></can1>
        </div>
        <div id="left-middle">
          <can2 v-if="has_can2" :key="can2_key"></can2>
        </div>
        <div id="left-bottom">
          <can3 v-if="has_can3" :key="can3_key"></can3>
        </div>
      </div>
      <!-- 视图中 -->
      <div class="body-middle">
        <div id="middle-top">
          <can4 v-if="has_data"></can4>
        </div>
        <div id="middle-bottom">
          <can5 v-if="has_can5" :key="can5_key"></can5>
        </div>
      </div>
      <!-- 视图右 -->
      <div class="body-right">
        <div id="right-top">
          <mol :key="mol_key"></mol>
        </div>
        <div id="right-bottom">
          <can6 v-if="has_can6" :key="can6_key"></can6>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue"
import API from '@/api/ajax.js'; // 引入API

export default {
  data() {
    return {
      // 左侧PDB说明信息
      pdb_info_ls: {
        // data1
        '1I7S': { // 1---
          name: '1I7S',
          info: 'ANTHRANILATE SYNTHASE FROM SERRATIA MARCESCENS IN COMPLEX WITH ITS END PRODUCT INHIBITOR L-TRYPTOPHAN',
          doiname: '10.2210/pdb1I7S/pdb',
          DOI: 'https://doi.org/10.2210/pdb1I7S/pdb',
          Classification: 'LYASE',
          Organism: 'Serratia marcescens',
          UniProt: 'P00897',
        },
        '1Z8D': { // 2---
          name: '1Z8D',
          info: 'Crystal Structure of Human Muscle Glycogen Phosphorylase a with AMP and Glucose',
          doiname: '10.2210/pdb1Z8D/pdb',
          DOI: 'https://doi.org/10.2210/pdb1Z8D/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'P11217',
        },
        '3EPS': { // 3---
          name: '3EPS',
          info: 'The crystal structure of isocitrate dehydrogenase kinase/phosphatase from E. coli',
          doiname: '10.2210/pdb3EPS/pdb',
          DOI: 'https://doi.org/10.2210/pdb3EPS/pdb',
          Classification: 'transferase, hydrolase',
          Organism: 'Escherichia coli O157:H7',
          UniProt: 'Q8X607',
        },
        '2BU2': { // 4---
          name: '2BU2',
          info: 'crystal structures of human pyruvate dehydrogenase kinase 2 containing physiological and synthetic ligands',
          doiname: '10.2210/pdb2BU2/pdb',
          DOI: 'https://doi.org/10.2210/pdb2BU2/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'Q15119',
        },
        '3RZ3': { // 5---
          name: '3RZ3',
          info: 'Human Cdc34 E2 in complex with CC0651 inhibitor',
          doiname: '10.2210/pdb3RZ3/pdb',
          DOI: 'https://doi.org/10.2210/pdb3RZ3/pdb',
          Classification: 'LIGASE/LIGASE INHIBITOR',
          Organism: 'Homo sapiens',
          UniProt: 'P49427',
        },
        '1PJ3': { // 6---
          name: '1PJ3',
          info: 'Crystal structure of human mitochondrial NAD(P)+-dependent malic enzyme in a pentary complex with natural substrate pyruvate, cofactor NAD+, Mn++, and allosteric activator fumarate.',
          doiname: '10.2210/pdb1PJ3/pdb',
          DOI: 'https://doi.org/10.2210/pdb1PJ3/pdb',
          Classification: 'OXIDOREDUCTASE',
          Organism: 'Homo sapiens',
          UniProt: 'P23368',
        },
        '3PTZ': { // 7---
          name: '3PTZ',
          info: 'Role of Packing Defects in the Evolution of Allostery and Induced Fit in Human UDP-Glucose Dehydrogenase.',
          doiname: '10.2210/pdb3PTZ/pdb',
          DOI: 'https://doi.org/10.2210/pdb3PTZ/pdb',
          Classification: 'OXIDOREDUCTASE',
          Organism: 'Homo sapiens',
          UniProt: 'O60701',
        },
        '2XO8': { // 8---
          name: '2XO8',
          info: 'Crystal Structure of Myosin-2 in Complex with Tribromodichloropseudilin',
          doiname: '10.2210/pdb2XO8/pdb',
          DOI: 'https://doi.org/10.2210/pdb2XO8/pdb',
          Classification: 'MOTOR PROTEIN',
          Organism: 'Dictyostelium discoideum',
          UniProt: 'P08799',
        },
        '2AL4': { // 9---
          name: '2AL4',
          info: 'CRYSTAL STRUCTURE OF THE GLUR2 LIGAND BINDING CORE (S1S2J) IN COMPLEX WITH quisqualate and CX614.',
          doiname: '10.2210/pdb2AL4/pdb',
          DOI: 'https://doi.org/10.2210/pdb2AL4/pdb',
          Classification: 'MEMBRANE PROTEIN',
          Organism: 'Rattus norvegicus',
          UniProt: 'P19491',
        },
        '1X88': { // 10---
          name: '1X88',
          info: 'Human Eg5 motor domain bound to Mg-ADP and monastrol',
          doiname: '10.2210/pdb1X88/pdb',
          DOI: 'https://doi.org/10.2210/pdb1X88/pdb',
          Classification: 'CELL CYCLE',
          Organism: 'Homo sapiens',
          UniProt: 'P52732',
        },
        '1FAP': { // 11---
          name: '1FAP',
          info: 'THE STRUCTURE OF THE IMMUNOPHILIN-IMMUNOSUPPRESSANT FKBP12-RAPAMYCIN COMPLEX INTERACTING WITH HUMAN FRAP',
          doiname: '10.2210/pdb1FAP/pdb',
          DOI: 'https://doi.org/10.2210/pdb1FAP/pdb',
          Classification: 'COMPLEX (ISOMERASE/KINASE)',
          Organism: 'Homo sapiens',
          UniProt: 'P62942',
        },
        '3H30': { // 12---
          name: '3H30',
          info: 'Crystal structure of the catalytic subunit of human protein kinase CK2 with 5,6-dichloro-1-beta-D-ribofuranosylbenzimidazole',
          doiname: '10.2210/pdb3H30/pdb',
          DOI: 'https://doi.org/10.2210/pdb3H30/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'P68400',
        },
        '1T49': { // 13---
          name: '1T49',
          info: 'Allosteric Inhibition of Protein Tyrosine Phosphatase 1B',
          doiname: '10.2210/pdb1T49/pdb',
          DOI: 'https://doi.org/10.2210/pdb1T49/pdb',
          Classification: 'HYDROLASE',
          Organism: 'Homo sapiens',
          UniProt: 'P18031',
        },
        '2C2B': { // 14---
          name: '2C2B',
          info: 'Crystallographic structure of Arabidopsis thaliana Threonine synthase complexed with pyridoxal phosphate and S-adenosylmethionine',
          doiname: '10.2210/pdb2C2B/pdb',
          DOI: 'https://doi.org/10.2210/pdb2C2B/pdb',
          Classification: 'LYASE',
          Organism: 'Arabidopsis thaliana',
          UniProt: 'Q9S7B5',
        },
        '3FZY': { // 15---
          name: '3FZY',
          info: 'Crystal Structure of Pre-cleavage Form of Cysteine Protease Domain from Vibrio cholerae RtxA Toxin',
          doiname: '10.2210/pdb3FZY/pdb',
          DOI: 'https://doi.org/10.2210/pdb3FZY/pdb',
          Classification: 'TOXIN',
          Organism: 'Vibrio cholerae',
          UniProt: 'Q9KS12',
        },
        '1W96': { // 16---
          name: '1W96',
          info: 'Crystal Structure of Biotin Carboxylase Domain of Acetyl-coenzyme A Carboxylase from Saccharomyces cerevisiae in Complex with SoraphenA',
          doiname: '10.2210/pdb1W96/pdb',
          DOI: 'https://doi.org/10.2210/pdb1W96/pdb',
          Classification: 'LIGASE',
          Organism: 'Saccharomyces cerevisiae',
          UniProt: 'Q00955',
        },
        '2R1R': { // 17---
          name: '2R1R',
          info: 'RIBONUCLEOTIDE REDUCTASE R1 PROTEIN WITH DTTP OCCUPYING THE SPECIFICITY SITE FROM ESCHERICHIA COLI',
          doiname: '10.2210/pdb2R1R/pdb',
          DOI: 'https://doi.org/10.2210/pdb2R1R/pdb',
          Classification: 'COMPLEX (OXIDOREDUCTASE/PEPTIDE)',
          Organism: 'Escherichia coli',
          UniProt: 'P00452',
        },
        '3PEE': { // 18---
          name: '3PEE',
          info: 'Structure of the C. difficile TcdB cysteine protease domain',
          doiname: '10.2210/pdb3PEE/pdb',
          DOI: 'https://doi.org/10.2210/pdb3PEE/pdb',
          Classification: 'TOXIN',
          Organism: 'Clostridioides difficile 630',
          UniProt: 'Q189K3',
        },
        // data2
        '4B2D': { // 1
          name: '4B2D',
          info: 'human PKM2 with L-serine and FBP bound.',
          doiname: '10.2210/pdb4B2D/pdb',
          DOI: 'https://doi.org/10.2210/pdb4B2D/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'P14618',
        },
        '3H6O': { // 2
          name: '3H6O',
          info: 'Activator-Bound Structure of Human Pyruvate Kinase M2',
          doiname: '10.2210/pdb3H6O/pdb',
          DOI: 'https://doi.org/10.2210/pdb3H6O/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'P14618',
        },
        '4G1N': { // 3
          name: '4G1N',
          info: 'PKM2 in complex with an activator',
          doiname: '10.2210/pdb4G1N/pdb',
          DOI: 'https://doi.org/10.2210/pdb4G1N/pdb',
          Classification: 'Transferase/Activator',
          Organism: 'Homo sapiens',
          UniProt: 'P14618',
        },
        '2YHD': { // 4
          name: '2YHD',
          info: 'Human androgen receptor in complex with AF2 small molecule inhibitor',
          doiname: '10.2210/pdb2YHD/pdb',
          DOI: 'https://doi.org/10.2210/pdb2YHD/pdb',
          Classification: 'TRANSCRIPTION',
          Organism: 'Homo sapiens',
          UniProt: 'P10275',
        },
        '2YLO': { // 5
          name: '2YLO',
          info: 'TARGETING THE BINDING FUNCTION 3 SITE OF THE ANDROGEN RECEPTOR THROUGH IN SILICO MOLECULAR MODELING',
          doiname: '10.2210/pdb2YLO/pdb',
          DOI: 'https://doi.org/10.2210/pdb2YLO/pdb',
          Classification: 'HORMONE RECEPTOR',
          Organism: 'Homo sapiens',
          UniProt: 'P10275',
        },
        '3O96': { // 6
          name: '3O96',
          info: 'Crystal Structure of Human AKT1 with an Allosteric Inhibitor',
          doiname: '10.2210/pdb3O96/pdb',
          DOI: 'https://doi.org/10.2210/pdb3O96/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'P31749',
        },
        '1GZ3': { // 7
          name: '1GZ3',
          info: 'Molecular mechanism for the regulation of human mitochondrial NAD(P)+-dependent malic enzyme by ATP and fumarate',
          doiname: '10.2210/pdb1GZ3/pdb',
          DOI: 'https://doi.org/10.2210/pdb1GZ3/pdb',
          Classification: 'OXIDOREDUCTASE',
          Organism: 'Homo sapiens',
          UniProt: 'P23368',
        },
        '4MDK': { // 8
          name: '4MDK',
          info: 'Cdc34-ubiquitin-CC0651 complex',
          doiname: '10.2210/pdb4MDK/pdb',
          DOI: 'https://doi.org/10.2210/pdb4MDK/pdb',
          Classification: 'LIGASE/LIGASE INHIBITOR',
          Organism: 'Homo sapiens',
          UniProt: 'P49427',
        },
        '3KCG': { // 9
          name: '3KCG',
          info: 'Crystal structure of the antithrombin-factor IXa-pentasaccharide complex',
          doiname: '10.2210/pdb3KCG/pdb',
          DOI: 'https://doi.org/10.2210/pdb3KCG/pdb',
          Classification: 'HYDROLASE, HYDROLASE INHIBITOR',
          Organism: 'Homo sapiens',
          UniProt: 'P00740',
        },
        '2XJC': { // 10
          name: '2XJC',
          info: 'Crystal structure of the D52N variant of cytosolic 5\'-nucleotidase II in complex with guanosine monophosphate and diadenosine tetraphosphate',
          doiname: '10.2210/pdb2XJC/pdb',
          DOI: 'https://doi.org/10.2210/pdb2XJC/pdb',
          Classification: 'HYDROLASE',
          Organism: 'Homo sapiens',
          UniProt: 'P49902',
        },
        '4BZB': { // 11
          name: '4BZB',
          info: 'Crystal structure of the tetrameric dGTP-bound SAMHD1 mutant catalytic core',
          doiname: '10.2210/pdb4BZB/pdb',
          DOI: 'https://doi.org/10.2210/pdb4BZB/pdb',
          Classification: 'HYDROLASE',
          Organism: 'Homo sapiens',
          UniProt: 'Q9Y3Z3',
        },
        '3PYY': { // 12
          name: '3PYY',
          info: 'Discovery and Characterization of a Cell-Permeable, Small-molecule c-Abl Kinase Activator that Binds to the Myristoyl Binding Site',
          doiname: '10.2210/pdb3PYY/pdb',
          DOI: 'https://doi.org/10.2210/pdb3PYY/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'P00519',
        },
        '4AW0': { // 13
          name: '4AW0',
          info: 'Human PDK1 Kinase Domain in Complex with Allosteric Compound PS182 Bound to the PIF-Pocket',
          doiname: '10.2210/pdb4AW0/pdb',
          DOI: 'https://doi.org/10.2210/pdb4AW0/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'O15530',
        },
        '3M6F': { // 14
          name: '3M6F',
          info: 'CD11A I-domain complexed with 6-((5S,9R)-9-(4-CYANOPHENYL)-3-(3,5-DICHLOROPHENYL)-1-METHYL-2,4-DIOXO-1,3,7- TRIAZASPIRO[4.4]NON-7-YL)NICOTINIC ACID',
          doiname: '10.2210/pdb3M6F/pdb',
          DOI: 'https://doi.org/10.2210/pdb3M6F/pdb',
          Classification: 'CELL ADHESION',
          Organism: 'Homo sapiens',
          UniProt: 'P20701',
        },
        '3ZCW': { // 15
          name: '3ZCW',
          info: 'Eg5 - New allosteric binding site',
          doiname: '10.2210/pdb3ZCW/pdb',
          DOI: 'https://doi.org/10.2210/pdb3ZCW/pdb',
          Classification: 'CELL CYCLE',
          Organism: 'Homo sapiens',
          UniProt: 'P52732',
        },
        '4BBG': { // 16
          name: '4BBG',
          info: 'Crystal structure of human kinesin Eg5 in complex with 3-(((2-Aminoethyl)sulfanyl)(3-ethylphenyl) phenylmethyl)phenol',
          doiname: '10.2210/pdb4BBG/pdb',
          DOI: 'https://doi.org/10.2210/pdb4BBG/pdb',
          Classification: 'CELL CYCLE',
          Organism: 'Homo sapiens',
          UniProt: 'P52732',
        },
        '3PXF': { // 17
          name: '3PXF',
          info: 'CDK2 in complex with two molecules of 8-anilino-1-naphthalene sulfonate',
          doiname: '10.2210/pdb3PXF/pdb',
          DOI: 'https://doi.org/10.2210/pdb3PXF/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'P24941',
        },
        '4G8O': { // 18
          name: '4G8O',
          info: 'Crystal Structure of a novel small molecule inactivator bound to plasminogen activator inhibitor-1',
          doiname: '10.2210/pdb4G8O/pdb',
          DOI: 'https://doi.org/10.2210/pdb4G8O/pdb',
          Classification: 'BLOOD CLOTTING/INHIBITOR',
          Organism: 'Aneurinibacillus thermoaerophilus',
          UniProt: 'P05121',
        },
        '4HSG': { // 19
          name: '4HSG',
          info: 'Crystal structure of human PRMT3 in complex with an allosteric inhibitor (PRMT3- KTD)',
          doiname: '10.2210/pdb4HSG/pdb',
          DOI: 'https://doi.org/10.2210/pdb4HSG/pdb',
          Classification: 'TRANSFERASE/TRANSFERASE INHIBITOR',
          Organism: 'Homo sapiens',
          UniProt: 'O60678',
        },
        '2BXA': { // 20
          name: '2BXA',
          info: 'Human serum albumin complexed with 3-carboxy-4-methyl-5-propyl-2- furanpropanoic acid (CMPF)',
          doiname: '10.2210/pdb2BXA/pdb',
          DOI: 'https://doi.org/10.2210/pdb2BXA/pdb',
          Classification: 'TRANSPORT PROTEIN',
          Organism: 'Homo sapiens',
          UniProt: 'P02768',
        },
        '1NSG': { // 21
          name: '1NSG',
          info: 'THE STRUCTURE OF THE IMMUNOPHILIN-IMMUNOSUPPRESSANT FKBP12-RAPAMYCIN COMPLEX INTERACTING WITH HUMAN FRAP',
          doiname: '10.2210/pdb1NSG/pdb',
          DOI: 'https://doi.org/10.2210/pdb1NSG/pdb',
          Classification: 'COMPLEX (ISOMERASE/KINASE)',
          Organism: 'Homo sapiens',
          UniProt: 'P62942',
        },
        '4EBW': { // 22
          name: '4EBW',
          info: 'Structure of Focal Adhesion Kinase catalytic domain in complex with novel allosteric inhibitor',
          doiname: '10.2210/pdb4EBW/pdb',
          DOI: 'https://doi.org/10.2210/pdb4EBW/pdb',
          Classification: 'TRANSFERASE/TRANSFERASE INHIBITOR',
          Organism: 'Homo sapiens',
          UniProt: 'Q05397',
        },
        '3N1V': { // 23
          name: '3N1V',
          info: 'Human FPPS COMPLEX WITH FBS_01',
          doiname: '10.2210/pdb3N1V/pdb',
          DOI: 'https://doi.org/10.2210/pdb3N1V/pdb',
          Classification: 'TRANSFERASE/TRANSFERASE INHIBITOR',
          Organism: 'Homo sapiens',
          UniProt: 'P14324',
        },
        '4E6C': { // 24
          name: '4E6C',
          info: 'p38a-perifosine Complex',
          doiname: '10.2210/pdb4E6C/pdb',
          DOI: 'https://doi.org/10.2210/pdb4E6C/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'Q16539',
        },
        '3HNC': { // 25
          name: '3HNC',
          info: 'Crystal structure of human ribonucleotide reductase 1 bound to the effector TTP',
          doiname: '10.2210/pdb3HNC/pdb',
          DOI: 'https://doi.org/10.2210/pdb3HNC/pdb',
          Classification: 'OXIDOREDUCTASE',
          Organism: 'Homo sapiens',
          UniProt: 'P23921',
        },
        '2BU6': { // 26
          name: '2BU6',
          info: 'crystal structures of human pyruvate dehydrogenase kinase 2 containing physiological and synthetic ligands',
          doiname: '10.2210/pdb2BU6/pdb',
          DOI: 'https://doi.org/10.2210/pdb2BU6/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'Q15119',
        },
        '2BU7': { // 27
          name: '2BU7',
          info: 'crystal structures of human pyruvate dehydrogenase kinase 2 containing physiological and synthetic ligands',
          doiname: '10.2210/pdb2BU7/pdb',
          DOI: 'https://doi.org/10.2210/pdb2BU7/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'Q15119',
        },
        '2BU8': { // 28
          name: '2BU8',
          info: 'crystal structures of human pyruvate dehydrogenase kinase 2 containing physiological and synthetic ligands',
          doiname: '10.2210/pdb2BU8/pdb',
          DOI: 'https://doi.org/10.2210/pdb2BU8/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Homo sapiens',
          UniProt: 'Q15119',
        },
        '4I1R': { // 29
          name: '4I1R',
          info: 'Human MALT1 (caspase-IG3) in complex with thioridazine',
          doiname: '10.2210/pdb4I1R/pdb',
          DOI: 'https://doi.org/10.2210/pdb4I1R/pdb',
          Classification: 'HYDROLASE/HYDROLASE INHIBITOR',
          Organism: 'Homo sapiens',
          UniProt: 'Q9UDY8',
        },
        '3QH0': { // 30
          name: '3QH0',
          info: 'X-ray crystal structure of palmitic acid bound to the cyclooxygenase channel of cyclooxygenase-2',
          doiname: '10.2210/pdb3QH0/pdb',
          DOI: 'https://doi.org/10.2210/pdb3QH0/pdb',
          Classification: 'OXIDOREDUCTASE',
          Organism: 'Mus musculus',
          UniProt: 'Q05769',
        },
        '3QOP': { // 31
          name: '3QOP',
          info: 'Domain-domain flexibility leads to allostery within the camp receptor protein (CRP)',
          doiname: '10.2210/pdb3QOP/pdb',
          DOI: 'https://doi.org/10.2210/pdb3QOP/pdb',
          Classification: 'DNA BINDING PROTEIN',
          Organism: 'Escherichia coli K-12',
          UniProt: 'P0ACJ8',
        },
        '3R1R': { // 32
          name: '3R1R',
          info: 'RIBONUCLEOTIDE REDUCTASE R1 PROTEIN WITH AMPPNP OCCUPYING THE ACTIVITY SITE FROM ESCHERICHIA COLI',
          doiname: '10.2210/pdb3R1R/pdb',
          DOI: 'https://doi.org/10.2210/pdb3R1R/pdb',
          Classification: 'COMPLEX (OXIDOREDUCTASE/PEPTIDE)',
          Organism: 'Escherichia coli, Escherichia coli (strain K12)',
          UniProt: 'P00452',
        },
        '1PCQ': { // 33
          name: '1PCQ',
          info: 'Crystal structure of groEL-groES',
          doiname: '10.2210/pdb1PCQ/pdb',
          DOI: 'https://doi.org/10.2210/pdb1PCQ/pdb',
          Classification: 'CHAPERONE',
          Organism: 'Escherichia coli',
          UniProt: 'P0A6F5',
        },
        '1H5S': { // 34
          name: '1H5S',
          info: 'Thymidylyltransferase complexed with TMP',
          doiname: '10.2210/pdb1H5S/pdb',
          DOI: 'https://doi.org/10.2210/pdb1H5S/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Escherichia coli',
          UniProt: 'P37744',
        },
        '1H9G': { // 35
          name: '1H9G',
          info: 'FadR, FATTY ACID RESPONSIVE TRANSCRIPTION FACTOR FROM E. COLI, in complex with myristoyl-CoA',
          doiname: '10.2210/pdb1H9G/pdb',
          DOI: 'https://doi.org/10.2210/pdb1H9G/pdb',
          Classification: 'TRANSCRIPTIONAL REGULATION',
          Organism: 'Escherichia coli',
          UniProt: 'P0A8V6',
        },
        '4P3H': { // 36
          name: '4P3H',
          info: 'Crystal structure of Kaposi\'s sarcoma-associated herpesvirus (KSHV) protease in complex with dimer disruptor',
          doiname: '10.2210/pdb4P3H/pdb',
          DOI: 'https://doi.org/10.2210/pdb4P3H/pdb',
          Classification: 'HYDROLASE',
          Organism: 'Human gammaherpesvirus 8',
          UniProt: 'O36607',
        },
        '1QP0': { // 37
          name: '1QP0',
          info: 'PURINE REPRESSOR-HYPOXANTHINE-PALINDROMIC OPERATOR COMPLEX',
          doiname: '10.2210/pdb1QP0/pdb',
          DOI: 'https://doi.org/10.2210/pdb1QP0/pdb',
          Classification: 'TRANSCRIPTION/DNA',
          Organism: 'Escherichia coli',
          UniProt: 'P0ACP7',
        },
        '2LDB': { // 38
          name: '2LDB',
          info: 'STRUCTURE DETERMINATION AND REFINEMENT OF BACILLUS STEAROTHERMOPHILUS LACTATE DEHYDROGENASE',
          doiname: '10.2210/pdb2LDB/pdb',
          DOI: 'https://doi.org/10.2210/pdb2LDB/pdb',
          Classification: 'OXIDOREDUCTASE(CHOH(D)-NAD(A))',
          Organism: 'Geobacillus stearothermophilus',
          UniProt: 'P00344',
        },
        '2JHR': { // 39
          name: '2JHR',
          info: 'Crystal structure of myosin-2 motor domain in complex with ADP- metavanadate and pentabromopseudilin',
          doiname: '10.2210/pdb2JHR/pdb',
          DOI: 'https://doi.org/10.2210/pdb2JHR/pdb',
          Classification: 'CONTRACTILE PROTEIN',
          Organism: 'Dictyostelium discoideum',
          UniProt: 'P08799',
        },
        '4KKO': { // 40
          name: '4KKO',
          info: 'Crystal Structure of HIV-1 Reverse Transcriptase in Complex with 4-((4-methoxy-6-(2-morpholinoethoxy)-1,3,5-triazin-2-yl)amino)-2-((3-methylbut-2-en-1-yl)oxy)benzonitrile (JLJ513), a non-nucleoside inhibitor',
          doiname: '10.2210/pdb4KKO/pdb',
          DOI: 'https://doi.org/10.2210/pdb4KKO/pdb',
          Classification: 'HYDROLASE/HYDROLASE INHIBITOR',
          Organism: 'Human immunodeficiency virus type 1 BH10',
          UniProt: 'P03366',
        },
        '4IG3': { // 41
          name: '4IG3',
          info: 'HIV-1 reverse transcriptase with bound fragment near Knuckles site',
          doiname: '10.2210/pdb4IG3/pdb',
          DOI: 'https://doi.org/10.2210/pdb4IG3/pdb',
          Classification: 'transferase/transferase inhibitor',
          Organism: 'Human immunodeficiency virus type 1 BH10',
          UniProt: 'P03366',
        },
        '4ETZ': { // 42
          name: '4ETZ',
          info: 'Crystal Structure of PelD 158-CT from Pseudomonas aeruginosa PAO1',
          doiname: '10.2210/pdb4ETZ/pdb',
          DOI: 'https://doi.org/10.2210/pdb4ETZ/pdb',
          Classification: 'SIGNALING PROTEIN',
          Organism: 'Pseudomonas aeruginosa PAO1',
          UniProt: 'Q9HZE7',
        },
        '4EAJ': { // 43
          name: '4EAJ',
          info: 'Co-crystal of AMPK core with AMP soaked with ATP',
          doiname: '10.2210/pdb4EAJ/pdb',
          DOI: 'https://doi.org/10.2210/pdb4EAJ/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Rattus norvegicus, Homo sapiens',
          UniProt: 'P54645',
        },
        '4MRA': { // 44
          name: '4MRA',
          info: 'Crystal structure of Gpb in complex with QUERCETIN',
          doiname: '10.2210/pdb4MRA/pdb',
          DOI: 'https://doi.org/10.2210/pdb4MRA/pdb',
          Classification: 'Transferase/transferase inhibitor',
          Organism: 'Oryctolagus cuniculus',
          UniProt: 'P00489',
        },
        '4OO9': { // 45
          name: '4OO9',
          info: 'Structure of the human class C GPCR metabotropic glutamate receptor 5 transmembrane domain in complex with the negative allosteric modulator mavoglurant',
          doiname: '10.2210/pdb4OO9/pdb',
          DOI: 'https://doi.org/10.2210/pdb4OO9/pdb',
          Classification: 'MEMBRANE PROTEIN',
          Organism: 'Homo sapiens, Tequatrovirus T4',
          UniProt: 'P41594',
        },
        '4EO6': { // 46
          name: '4EO6',
          info: 'HCV NS5B polymerase inhibitors: Tri-substituted acylhydrazines as tertiary amide bioisosteres',
          doiname: '10.2210/pdb4EO6/pdb',
          DOI: 'https://doi.org/10.2210/pdb4EO6/pdb',
          Classification: 'TRANSFERASE/TRANSFERASE INHIBITOR',
          Organism: 'Hepatitis C virus (isolate BK)',
          UniProt: 'P26663',
        },
        '4NLD': { // 47
          name: '4NLD',
          info: 'Crystal structure of the hepatitis C virus NS5B RNA-dependent RNA polymerase complex with BMS-791325 also known as (1aR,12bS)-8-cyclohexyl-n-(dimethylsulfamoyl)-11-methoxy-1a-{[(1R,5S)-3-methyl-3,8-diazabicyclo[3.2.1]oct-8-yl]carbonyl}-1,1a,2,12b-tetrahydrocyclopropa[d]indolo[2,1-a][2]benzazepine-5-carboxamide and 2-(4-fluorophenyl)-n-methyl-6-[(methylsulfonyl)amino]-5-(propan-2-yloxy)-1-benzofuran-3-carboxamide',
          doiname: '10.2210/pdb4NLD/pdb',
          DOI: 'https://doi.org/10.2210/pdb4NLD/pdb',
          Classification: 'transferase/transferase INHIBITOR',
          Organism: 'Hepatitis C virus (isolate Con1)',
          UniProt: 'Q9WMX2',
        },
        '1XJF': { // 48
          name: '1XJF',
          info: 'Structural mechanism of allosteric substrate specificity in a ribonucleotide reductase: dATP complex',
          doiname: '10.2210/pdb1XJF/pdb',
          DOI: 'https://doi.org/10.2210/pdb1XJF/pdb',
          Classification: 'OXIDOREDUCTASE',
          Organism: 'Thermotoga maritima',
          UniProt: 'O33839',
        },
        '4B1F': { // 49
          name: '4B1F',
          info: 'Design of Inhibitors of Helicobacter pylori Glutamate Racemase as Selective Antibacterial Agents: Incorporation of Imidazoles onto a Core Pyrazolopyrimidinedione Scaffold to Improve Bioavailabilty',
          doiname: '10.2210/pdb4B1F/pdb',
          DOI: 'https://doi.org/10.2210/pdb4B1F/pdb',
          Classification: 'ISOMERASE',
          Organism: 'Helicobacter pylori',
          UniProt: 'Q9ZLT0',
        },
        '2W4I': { // 50 
          name: '2W4I',
          info: 'Crystal structure of Helicobacter pylori glutamate racemase in complex with D-Glutamate and an inhibitor',
          doiname: '10.2210/pdb2W4I/pdb',
          DOI: 'https://doi.org/10.2210/pdb2W4I/pdb',
          Classification: 'ISOMERASE',
          Organism: 'Helicobacter pylori',
          UniProt: 'Q9ZLT0',
        },
        '4BQH': { // 51
          name: '4BQH',
          info: 'Crystal structure of the uridine diphosphate N-acetylglucosamine pyrophosphorylase from Trypanosoma brucei in complex with inhibitor',
          doiname: '10.2210/pdb4BQH/pdb',
          DOI: 'https://doi.org/10.2210/pdb4BQH/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Trypanosoma brucei',
          UniProt: 'Q386Q8',
        },
        '1JLR': { // 52
          name: '1JLR',
          info: 'STRUCTURE OF THE URACIL PHOSPHORIBOSYLTRANSFERASE GTP COMPLEX 2 MUTANT C128V',
          doiname: '10.2210/pdb1JLR/pdb',
          DOI: 'https://doi.org/10.2210/pdb1JLR/pdb',
          Classification: 'TRANSFERASE',
          Organism: 'Toxoplasma gondii',
          UniProt: 'Q26998',
        },
        '4MBS': { // 53
          name: '4MBS',
          info: 'Crystal Structure of the CCR5 Chemokine Receptor',
          doiname: '10.2210/pdb4MBS/pdb',
          DOI: 'https://doi.org/10.2210/pdb4MBS/pdb',
          Classification: 'SIGNALING PROTEIN',
          Organism: 'Homo sapiens, Clostridium pasteurianum',
          UniProt: 'P51681',
        },
        '2VPR': { // 54
          name: '2VPR',
          info: 'Tet repressor class H in complex with 5a,6- anhydrotetracycline-Mg',
          doiname: '10.2210/pdb2VPR/pdb',
          DOI: 'https://doi.org/10.2210/pdb2VPR/pdb',
          Classification: 'TRANSCRIPTION',
          Organism: 'Pasteurella multocida',
          UniProt: 'P51561',
        },
        '3HO6': { // 55
          name: '3HO6',
          info: 'Structure-function analysis of inositol hexakisphosphate-induced autoprocessing in clostridium difficile toxin A',
          doiname: '10.2210/pdb3HO6/pdb',
          DOI: 'https://doi.org/10.2210/pdb3HO6/pdb',
          Classification: 'TOXIN',
          Organism: 'Clostridioides difficile',
          UniProt: 'P16154',
        },
      },
      // fea_ls_val:['Score','Number of Alpha Spheres','gnm60','Volume','Polarity score'], // 重要特征列表
      // fea_ls:['pScore','pAnum','pGnm60','pVolume','pPolsc'], // 重要特征列表
      data_train: null,// 训练集数据
      pdbName: null,
      poc1: 1,
      poc2: 2,
      viewerContainer: null,
      options: null,
      // 数据更新标记
      PocketAtomsFlag: false,
      data_trainFlag: false,
      PDBPocFlag: false,
      zxposFlag: false,
      posTSNEFlag: false,
    }
  },
  components: {
    can1: defineAsyncComponent(() => import("@/components/can1/can1.vue")),
    can2: defineAsyncComponent(() => import("@/components/can2/can2.vue")),
    can3: defineAsyncComponent(() => import("@/components/can3/can3.vue")),
    mol: defineAsyncComponent(() => import("@/components/mol/mol.vue")),
    can4: defineAsyncComponent(() => import("@/components/can4/can4.vue")),
    can5: defineAsyncComponent(() => import("@/components/can5/can5.vue")),
    can6: defineAsyncComponent(() => import("@/components/can6/can6.vue")),
  },
  mounted() {
    // 获取口袋名称
    this.pdbName = this.$store.state.pdbName
    // 1 获取口袋原子
    this.getPDBAtom()
    // 2 获取data_train数据
    API({
      url: '/api/data_train.json',
      method: 'get'
    }).
    then((res) => {
      let recvdata = res.data
      this.data_train = recvdata // 这是训练集的数据
      this.$store.commit('changeDataTrain', this.data_train) // 更新数据
      this.data_trainFlag = true
    })
    // 3 获取蛋白质特征信息
    this.getPDBData(this.$store.state.pdbName)
    // 4 获取口袋质心位置数据（poc_zxpos.json）
    API({
      url: '/api/poc_zxpos.json',
      method: 'get'
    }).
    then((res) => {
      let recvdata = res.data
      this.$store.commit('changezxpos',recvdata) // 更新口袋质心文件
      this.zxposFlag = true
    })
    // 5 获取口袋质心+中心的相关数据
    API({
      url: '/api/poc_posTSNE.json',
      method: 'get'
    }).
    then((res) => {
      let recvdata = res.data
      this.$store.commit('changeposTSNE',recvdata) // 更新口袋质心文件
      this.posTSNEFlag = true
    })
  },
  methods: {
    getPDBData(name) {
      // 根据蛋白质名称，获取蛋白质的口袋数据
      API({
        url: '/api/pdb/' + name + '_info.json',// 获取不同蛋白质的信息
        method: 'get'
      }).then((res) => {
        let recvdata = res.data
        this.$store.commit('changePDBPoc',recvdata)
        this.$store.commit('changePDBName',name)
        this.PDBPocFlag = true
      })
    },
    // 获取口袋原子信息
    getPDBAtom() {
      API({
        url: '/api/poc_atoms.json',
        method: 'get'
      }).then((res) => {
        let recvdata = res.data
        this.$store.commit('changePocketAtoms',recvdata)
        this.PocketAtomsFlag = true
      })
    },
  },
  computed: {
    // 用于更新can1
    can1_key() {
      return this.PocketAtomsFlag.toString() +
      this.data_trainFlag.toString() +
      this.PDBPocFlag.toString() +
      this.zxposFlag.toString() +
      this.posTSNEFlag.toString() +
      this.$store.state.pocChoice.toString()
    },
    // 是否接受完数据
    has_data() {
      return this.PocketAtomsFlag &&
      this.data_trainFlag &&
      this.PDBPocFlag &&
      this.zxposFlag &&
      this.posTSNEFlag
    },
    // 更新can2
    has_can2() {
      return this.$store.state.can1SelAllo.length > 0 ||
      this.$store.state.can1SelnoAllo.length > 0
    },
    can2_key() {
      return this.$store.state.can1SelAllo.join(',') +
      this.$store.state.can1SelnoAllo.join(',') +
      this.$store.state.pocChoice.toString() +
      this.$store.state.can1ShowTextAllo.join(',') +
      this.$store.state.can1ShowTextnoAllo.join(',')
    },
    // 更新can3
    has_can3() {
      return this.$store.state.can1SelAllo.length > 0 ||
      this.$store.state.can1SelnoAllo.length > 0
    },
    can3_key() {
      return this.$store.state.can1SelAllo.join(',') +
      this.$store.state.can1SelnoAllo.join(',') +
      this.$store.state.pocChoice.toString() +
      this.$store.state.can1ShowTextAllo.join(',') +
      this.$store.state.can1ShowTextnoAllo.join(',') +
      this.$store.state.can2Selnode.toString() +
      this.$store.state.can2Seledge.join(',')
    },
    // 更新mol
    mol_key() {
      return this.$store.state.pdbName +
      this.$store.state.pocChoice.toString()
    },
    // 更新can5
    has_can5() {
      return this.$store.state.can1SelAllo.length > 0 ||
      this.$store.state.can1SelnoAllo.length > 0
    },
    can5_key() {
      return this.$store.state.can1SelAllo.join(',') +
      this.$store.state.can1SelnoAllo.join(',') +
      this.$store.state.pocChoice.toString()
    },
    // 更新can6
    has_can6() {
      return this.posTSNEFlag
    },
    can6_key() {
      return this.$store.state.pdbName
    },
  },
  watch: {
    splitNum: function(newValue,oldValue) {
      if(newValue != oldValue) {
        this.$store.commit('changeSplitNum',newValue)
        // 1、更新pic1的数据
        // 2、更新pic2的数据
        this.sn_fea
      }
    },
    now_fea: function(newValue,oldValue) {
      if(newValue != oldValue) {
        this.$store.commit('changeNowFea',newValue)
        // 1、更新pic1的数据
        // 2、更新pic2的数据
        this.sn_fea
      }
    },
    pdbName: function(newValue,oldValue) {
      if(newValue != null && newValue != undefined && newValue.length === 4) {
        if(newValue != oldValue) {
          // 删除选择的口袋
          this.$store.commit('changePocChoice',-1)
          // 更新值
          this.getPDBData(newValue)
        }
      }
    },
  }
}
</script>

<style lang="less" scoped>
.com-container {
  height: 100%;
  width: 100%;
  display: flex;
  position: relative;
  flex-direction: column;
  justify-content: space-between;
}
.com-header {
  height: 10%;
  width: 100%;
  display: flex;
  position: relative;
  background-color: rgb(245, 244, 244);
  flex-direction: row;
  justify-content: space-between;
}
.com-body {
  height: 90%;
  width: 100%;
  display: flex;
  position: relative;
  flex-direction: row;
  justify-content: space-between;
  .com-navig {
    width: 10%;
    height: calc(17px + 90%);
    border:2px solid grey;
    background-color:#E6E6E6;
    margin-left: 5px;
  }
  .body-left {
    height: 100%;
    width: 28%;
    #left-top {
      height:30%;
      border:2px solid grey;
    }
    #left-middle {
      height:30%;
      border:2px solid grey;
      margin-top: 5px;
    }
    #left-bottom {
      height: 30%;
      margin-top: 5px;
      border:2px solid grey;
      position: relative;
    }
  }
  .body-middle {
    height: 100%;
    width: 30%;
    #middle-top {
      width: 100%;
      height: 45%;
      position: relative;
      border:2px solid grey;
    }
    #middle-bottom {
      margin-top: 5px;
      width: 100%;
      height: calc(9px + 45%);
      border:2px solid grey;
      position: relative;
    }
  }
  .body-right {
    height: 100%;
    width: 30%;
    margin-right: 5px;
    position: relative;
    #right-top {
      height: 45%;
      border:2px solid grey;
      position: relative;
      z-index: 3;
    }
    #right-bottom {
      height: calc(9px + 45%);
      margin-top: 5px;
      border:2px solid grey;
      position: relative;
      z-index: 2;
    }
  }
}

.title {
  position: relative;
  left: 50%;
  top: 50%;
  font-size: 20px;
  transform: translate(-50%, -50%);
}
</style>