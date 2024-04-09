<template>
  <div class="main-div">
    <h2>{{ heading }}</h2>
    <div class="cards d-flex flex-wrap">
      <Card v-for="(book, index) in books" :key="index" :book="book" />
      <p v-if="books.length === 0">You Dont Have Any {{ heading }}</p>
    </div>
  </div>
</template>

<script>
import Card from "@/components/Card.vue";
import { jwtDecode } from "jwt-decode";
import axios from "axios";

export default {
  name: "Issued",
  props: ["heading"],
  components: { Card },
  data() {
    return {
      books: [],
    };
  },
  mounted() {
    this.fetchBooks();
  },

  methods: {
    async fetchBooks() {
      const accessToken = localStorage.getItem("accessToken");

      if (!accessToken) {
        console.error("Access token not found in localStorage");
        return;
      }

      const decodedToken = jwtDecode(accessToken);
      const user_id = decodedToken.sub;

      try {
        const issuedBooksResponse = await axios.get(
          `http://127.0.0.1:5000/issued-books/${user_id}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.books = issuedBooksResponse.data;
      } catch (error) {
        console.error("Error fetching issued books:", error);
      }
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
