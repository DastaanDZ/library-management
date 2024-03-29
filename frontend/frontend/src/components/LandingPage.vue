<template>
  <div class="parent-div">
    <Navbar />
    <div class="main-page">
      <UserDetail />
      <NewArrival />
      <BooksAvailable />
      <BookIssued />
      <BookRequested />
      <BookReturned />
    </div>
  </div>
</template>

<script>
import Navbar from "./Navbar.vue";
import NewArrival from "./NewArrival.vue";
import BookIssued from "./BookIssued.vue";
import BookRequested from "./BookRequested.vue";
import BookReturned from "./BookReturned.vue";
import BooksAvailable from "./BooksAvailable.vue";
import UserDetail from "./UserDetail.vue";

export default {
  name: "LandingPage",
  components: {
    Navbar,
    UserDetail,
    BookIssued,
    BookRequested,
    BookReturned,
    BooksAvailable,
    NewArrival,
  },
};
</script>

<style scoped>
.parent-div {
  display: flex;
  flex-direction: column;
  padding: 0 2rem;
  gap: 2rem;
}
.main-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>
