<template>
  <div>
    <Navbar />
    <div class="main-page">
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

export default {
  name: "LandingPage",
  components: {
    Navbar,
    BookIssued,
    BookRequested,
    BookReturned,
    BooksAvailable,
    NewArrival,
  },
};
</script>

<style scoped>
.main-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
}
</style>
