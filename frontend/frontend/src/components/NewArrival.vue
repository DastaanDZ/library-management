<template>
  <div
    id="carouselExampleAutoplaying"
    class="carousel slide"
    data-bs-ride="carousel"
  >
    <h2>New Arrival</h2>
    <div class="carousel-inner">
      <div class="carousel-item active">
        <img src="./book.jpg" class="d-block" alt="" />
      </div>
      <div class="carousel-item">
        <img src="./book.jpg" class="d-block" alt="" />
      </div>
      <div class="carousel-item">
        <img src="./book.jpg" class="d-block" alt="" />
      </div>
    </div>
    <button
      class="carousel-control-prev"
      type="button"
      data-bs-target="#carouselExampleAutoplaying"
      data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
      class="carousel-control-next"
      type="button"
      data-bs-target="#carouselExampleAutoplaying"
      data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script>
export default {
  name: "NewArrival",
};
</script>

<style scoped>
.carousel {
  background-color: white;
  padding: 2rem 0;
  border-radius: 1rem;
}
.carousel-inner {
  padding: 0 5rem;
}
.carousel-item img {
  width: 15rem;
  height: 25rem;
}
</style>
