<template>
  <div class="welcome-page">
    <h1>Welcome to Library Management Application</h1>
  </div>
</template>

<script>
export default {
  name: "Home",
  mounted() {
    setTimeout(() => {
      this.$router.push("/login");
    }, 2000);
  },
};
</script>

<style scoped>
.welcome-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.welcome-page h1 {
  font-size: 24px;
}
</style>
