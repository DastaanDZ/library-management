<template>
  <div class="add-book-form">
    <h1>Add Book</h1>
    <form @submit.prevent="addBook">
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
      <UploadWidget @incomingUrl="receiveUrl" />
      <img width="400" id="uploadedimage" src="" />
      <div class="form-group text-start mb-1">
        <button type="submit" class="btn btn-block create-account">
          Add Book
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import UploadWidget from "@/components/UploadWidget.vue";

export default {
  name: "AddBookForm",
  components: {
    UploadWidget,
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
        selectedFile: null,
      },
    };
  },
  mounted() {
    const userRole = localStorage.getItem("role");
    if (userRole !== "librarian") {
      this.$router.push("/librarian");
    }
  },
  methods: {
    async addBook() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        if (
          !this.bookData.name ||
          !this.bookData.content ||
          !this.bookData.author ||
          !this.bookData.count ||
          !this.bookData.price ||
          !this.bookData.selectedFile
        ) {
          return;
        }
        console.log(this.bookData);
        await axios.post("http://127.0.0.1:5000/add-book", this.bookData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.resetFormData();
        alert("Book added successfully");
        window.location.reload();
      } catch (error) {
        console.error("Error adding book:", error);
        if (error.response && error.response.status === 401) {
          window.location.href = "/login";
        }
      }
    },
    resetFormData() {
      this.bookData = {
        name: "",
        content: "",
        author: "",
        count: 0,
        available: false,
        price: 0,
        selectedFile: null,
      };
    },
    onFileSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    receiveUrl(url) {
      console.log("Received URL", url);
      this.bookData.selectedFile = url;
    },
  },
};
</script>

<style>
.add-book-form {
  padding: 50px 0;
}

.add-book-form form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.add-book-form .form-group {
  margin-bottom: 20px;
}

.add-book-form .item {
  border-radius: 20px;
  padding: 10px 20px;
}

.add-book-form .create-account {
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
  .add-book-form form {
    padding: 50px 20px;
  }
}
</style>
