<template>
  <div class="card mb-3">
    <div class="row g-0">
      <div class="col-md-4">
        <img
          src="./book.jpg"
          class="img-fluid rounded-start"
          alt="img not found"
        />
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <p class="card-text">
            This is a wider card with supporting text below as a natural lead-in
            to additional content. This content is a little bit longer.
          </p>
          <p class="card-text">
            <small class="text-body-secondary">Last updated 3 mins ago</small>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardDetails",
};
</script>

<style scoped>
.card {
  width: 100%;
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  border: none;
}
.card-body {
  height: 30rem;
}
.row {
  width: 60rem;
  height: auto;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 0.375rem;
}
</style>
