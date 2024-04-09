<template>
  <div class="edit-book-form">
    <h1>Edit Book</h1>
    <form @submit.prevent="editBook">
      <div class="form-group text-start mb-1">
        <label for="name">Name:</label>
        <input
          v-model="bookData.name"
          type="text"
          class="form-control item"
          id="name"
          placeholder="Book Name"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="content">Content:</label>
        <textarea
          v-model="bookData.content"
          class="form-control item"
          id="content"
          rows="5"
          placeholder="Book Content"
        ></textarea>
      </div>
      <div class="form-group text-start mb-1">
        <label for="author">Author:</label>
        <input
          v-model="bookData.author"
          type="text"
          class="form-control item"
          id="author"
          placeholder="Book Author"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="count">Count:</label>
        <input
          v-model.number="bookData.count"
          type="number"
          class="form-control item"
          id="count"
          placeholder="Book Count"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="available">Available:</label>
        <input
          type="checkbox"
          v-model="bookData.available"
          class="form-check-input"
          id="available"
        />
        <label class="form-check-label" for="available"></label>
      </div>
      <div class="form-group text-start mb-1">
        <label for="price">Price:</label>
        <input
          v-model.number="bookData.price"
          type="number"
          class="form-control item"
          id="price"
          placeholder="Book Price"
        />
      </div>
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-block update-book">
          Update Book
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EditBook",
  props: {
    bookId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      bookData: {
        name: "",
        content: "",
        author: "",
        count: 0,
        available: false,
        price: 0,
      },
    };
  },
  mounted() {
    this.fetchBook();
  },
  methods: {
    async fetchBook() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/books/${this.$route.params.book_id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.bookData = response.data;
      } catch (error) {
        console.error("Error fetching book:", error);
      }
    },
    async editBook() {
      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/edit-book/${this.$route.params.book_id}`,
          this.bookData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        console.log(response.data);
        alert("Book updates successfully");
        // Optionally, you can add a success message or redirect to another page
      } catch (error) {
        console.error("Error editing book:", error);
      }
    },
  },
};
</script>

<style scoped>
.edit-book-form {
  padding: 50px 0;
}

.edit-book-form form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.edit-book-form .form-group {
  margin-bottom: 20px;
}

.edit-book-form .item {
  border-radius: 20px;
  padding: 10px 20px;
}

.edit-book-form .update-book {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: bold;
  background-color: #5791ff;
  border: none;
  color: white;
  margin-top: 20px;
}

@media (max-width: 576px) {
  .edit-book-form form {
    padding: 50px 20px;
  }
}
</style>
