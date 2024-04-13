<template>
  <div class="card d-flex flex-wrap">
    <img :src="book.link" class="card-img-top" alt="Book Cover" />
    <div class="card-body">
      <h5 class="card-title">{{ book.name }}</h5>
      <h6 class="card-subtitle">{{ book.author }}</h6>
    </div>
    <router-link
      :to="{
        name: userRole === 'librarian' ? 'LibCardDetails' : 'CardDetails',
        params: {
          book_id: book.book_id ? book.book_id : book.id,
        },
      }"
    >
      <button class="btn btn-primary mt-3" type="submit">View Details</button>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: {
    book: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      userRole: localStorage.getItem("role"),
    };
  },
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
