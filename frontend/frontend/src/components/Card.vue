<template>
  <div class="card">
    <img src="./book.jpg" class="card-img-top" alt="img not found" />
    <div class="card-body">
      <h5 class="card-title">Card title</h5>
      <h6 class="card-title">Card subtitle</h6>
      <p class="card-text">due date</p>
      <a href="#" class="btn btn-primary"
        ><router-link :to="{ name: 'CardDetails' }"
          >Go somewhere</router-link
        ></a
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "Card",
};
</script>

<style scoped>
.card {
  border: none;
  width: 14rem;
}
.btn-primary a {
  color: white;
  text-decoration: none;
}
</style>
