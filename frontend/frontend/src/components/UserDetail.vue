<template>
  <div class="parent">
    <div class="main">
      <div class="user-div">
        <div class="dp">
          <img src="./book.jpg" alt="" />
        </div>
        <h3>Hello, User Name</h3>
      </div>
      <button type="button" class="btn btn-primary">
        Edit Personal<br />Details
      </button>
    </div>
  </div>
</template>
<script>
export default {
  name: "UserDetail",
};
</script>

<style scoped>
.parent {
  padding: 0 2rem;
}
.main {
  display: flex;
  align-items: center;
  padding: 0 2rem;
  justify-content: space-between;
  background: white;
  border-radius: 2rem;
}
.edit {
  width: 10rem;
  height: 10rem;
  display: flex;
  align-items: end;
  justify-content: center;
  padding: 1rem;
}
.user-div {
  display: flex;
  gap: 2rem;
  padding: 2rem 2rem;
  width: 40rem;
  align-items: center;
}
.dp {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
  border: 2px solid black;
  overflow: hidden;
}
.dp img {
  object-fit: cover;
  width: 100%;
  height: 100%;
}
</style>
