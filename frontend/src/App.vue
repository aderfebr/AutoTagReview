<template>
  <div id="bg">
    <vue-particles
        color="#39AFFD"
        :particleOpacity="0.7"
        :particlesNumber="80"
        shapeType="circle"
        :particleSize="4"
        linesColor="#39AFFD"
        :linesWidth="1"
        :lineLinked="true"
        :lineOpacity="0.4"
        :linesDistance="150"
        :moveSpeed="2"
        :hoverEffect="true"
        hoverMode="grab"
        :clickEffect="false"
        clickMode="push"
      >
    </vue-particles>
    <RouterView></RouterView>
  </div>
</template>

<script>

</script>

<style>
*{
    padding: 0;
    margin: 0;
}
#bg{
    width: 100vw;
    height: 100vh;
    background: #fff;
}
#particles-js{
    width: 100%;
    height: 100%;
    position: absolute;
    overflow: hidden;
}
</style>
