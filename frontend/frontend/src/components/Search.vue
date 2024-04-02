<template>
  <div>
    <input v-model="searchQuery" type="text" placeholder="Search..." />
    <button @click="searchSections">Search Sections</button>
    <button @click="searchBooks">Search Books</button>

    <!-- Display search results -->
    <div v-for="result in searchResults" :key="result.id">
      <h3>{{ result.name }}</h3>
      <p>{{ result.description }}</p>
      <!-- Display associated books -->
      <ul>
        <li v-for="book in result.books" :key="book.id">
          {{ book.name }} - {{ book.author }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Search",
  data() {
    return {
      searchQuery: "",
      searchResults: [],
    };
  },
  methods: {
    searchSections() {
      axios
        .get(`http://127.0.0.1:5000/sections?query=${this.searchQuery}`)
        .then((response) => {
          this.searchResults = response.data;
        })
        .catch((error) => {
          console.error("Error searching sections:", error);
        });
    },
    searchBooks() {
      axios
        .get(`http://127.0.0.1:5000/books?query=${this.searchQuery}`)
        .then((response) => {
          this.searchResults = response.data;
        })
        .catch((error) => {
          console.error("Error searching books:", error);
        });
    },
  },
};
</script>
