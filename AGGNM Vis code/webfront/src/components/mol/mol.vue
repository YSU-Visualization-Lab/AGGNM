<template>
  <div style="width: 100%;height: 100%;">
    <div style="background-color:#A8A8A8; font-size: 10px; text-align:center"><b>Pocket 3D structure plot</b></div>
    <div id="pdbView" style="width: 100%;height: 96%;">
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      viewerInstance: null,
      viewerContainer: null,
      optionBall: null,
    }
  }, 
  mounted() {
    this.initMolStart()
  }, 
  methods: {
    initMolStart() {
      let URL = 'http://127.0.0.1:7777/api/poc_pdb/' + this.$store.state.pdbName + "/" + "pocket_" + (this.$store.state.pocChoice + 1).toString() + '.pdb'
      if(this.$store.state.pocChoice === -1)
      {
        URL = 'http://127.0.0.1:7777/api/poc_pdb/' + this.$store.state.pdbName + "/" + this.$store.state.pdbName + '.pdb'
      }
      let that = this;
      that.viewerInstance = new PDBeMolstarPlugin();
      that.viewerContainer = document.getElementById("pdbView")
      that.optionBall = {
        customData: {
          url: URL,
          format: "pdb",
        },
        hideControls: true, 
        landscape: false,
      }
      that.viewerInstance.render(that.viewerContainer, that.optionBall)
    },
  }
}
</script>

<style scoped>

#pdbView {
  width: 100%;
  height: 100%;
  background: #555555;
  position: relative;
}
</style>
