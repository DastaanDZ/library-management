<template>
  <div class="main-div">
    <h2>{{ heading }}</h2>
    <div class="cards">
      <Card
        v-for="(book, index) in books.slice(0, 5)"
        :key="index"
        :book="book"
      />
      <p v-if="books.length === 0">You Dont Have Any {{ heading }}</p>
    </div>
    <h6>
      <a
        ><router-link
          :to="{ name: 'ViewAll', props: { books: books, heading: heading } }"
        >
          <button class="btn btn-primary" type="submit">View All</button>
        </router-link></a
      >
    </h6>
  </div>
</template>

<script>
import Card from "./Card.vue";

export default {
  name: "BooksAvailable",
  components: { Card },
  props: {
    books: {
      type: Array,
      required: true,
    },
    heading: {
      type: String,
    },
  },
};
</script>

<style scoped>
.cards {
  display: flex;
  gap: 2rem;
  width: 100%;
  justify-content: center;
}
.main-div {
  display: flex;
  align-items: start;
  flex-direction: column;
  padding: 2rem;
  background-color: white;
  border-radius: 1rem;
  gap: 1rem;
}
.main-div h6 {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.main-div h6 a {
  cursor: pointer;
  display: flex;
  justify-content: center;
}
.main-div h6 a:hover {
  color: blue;
}
</style>
