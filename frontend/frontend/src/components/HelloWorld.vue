<template>
  <div class="main-div">
    <h2>Book Issued</h2>
    <div class="cards">
      <div class="card">
        <img src="./book.jpg" class="card-img-top" alt="img not found" />
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <h6 class="card-title">Card subtitle</h6>
          <p class="card-text">due date</p>
          <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
      <div class="card">
        <img src="./book.jpg" class="card-img-top" alt="img not found" />
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <h6 class="card-title">Card subtitle</h6>
          <p class="card-text">due date</p>
          <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
      <div class="card">
        <img src="./book.jpg" class="card-img-top" alt="img not found" />
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <h6 class="card-title">Card subtitle</h6>
          <p class="card-text">due date</p>
          <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.cards {
  display: flex;
  gap: 2rem;
}
.card {
  border: none;
  width: 12rem;
}
.main-div {
  display: flex;
  align-items: start;
  flex-direction: column;
}
</style>
