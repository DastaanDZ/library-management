<template>
  <div class="assign-section-page">
    <h1>Assign Book to Section</h1>
    <form @submit.prevent="assignBook">
      <div class="form-group text-start mb-1">
        <label for="book">Select Book:</label>
        <select v-model="selectedBook" class="form-control item" id="book">
          <option v-for="book in books" :key="book.id" :value="book.id">
            {{ book.name }}
          </option>
        </select>
      </div>
      <div class="form-group text-start mb-1">
        <label for="section">Select Section:</label>
        <select
          v-model="selectedSection"
          class="form-control item"
          id="section"
        >
          <option
            v-for="section in sections"
            :key="section.id"
            :value="section.id"
          >
            {{ section.name }}
          </option>
        </select>
      </div>
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-primary create-account">
          Assign Book
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AssignSection",
  data() {
    return {
      selectedBook: null,
      selectedSection: null,
      books: [],
      sections: [],
    };
  },
  async mounted() {
    await this.fetchBooks();
    await this.fetchSections();
  },
  methods: {
    async fetchBooks() {
      try {
        const accessToken = localStorage.getItem("accessToken");

        const response = await axios.get("http://127.0.0.1:5000/books", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.books = response.data;
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    },
    async fetchSections() {
      try {
        const accessToken = localStorage.getItem("accessToken");

        const response = await axios.get("http://127.0.0.1:5000/sections", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.sections = response.data.sections;
      } catch (error) {
        console.error("Error fetching sections:", error);
      }
    },
    async assignBook() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await axios.post(
          `http://127.0.0.1:5000/assign-book/${this.selectedBook}/${this.selectedSection}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        alert("Book assigned to section successfully");
      } catch (error) {
        console.error("Error assigning book to section:", error);
      }
    },
  },
};
</script>

<style>
.assign-section-page {
  padding: 50px 0;
}

.assign-section-page form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.assign-section-page .form-group {
  margin-bottom: 20px;
}

.assign-section-page .item {
  border-radius: 20px;
  padding: 10px 20px;
}

.assign-section-page .create-account {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: bold;
  background-color: #5791ff;
  border: none;
  color: white;
  margin-top: 20px;
}
</style>
