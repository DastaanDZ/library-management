<template>
  <div class="card">
    <img src="./book.jpg" class="card-img-top" alt="Book Cover" />
    <div class="card-body">
      <h5 class="card-title">{{ book.name }}</h5>
      <h6 class="card-subtitle">{{ book.author }}</h6>
      <router-link
        :to="{
          name: 'CardDetails',
          params: { book_id: book.book_id ? book.book_id : book.id },
        }"
      >
        View Details
      </router-link>
    </div>
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
