<template>
  <div class="registration-form">
    <h1>ADD BOOKS</h1>
    <form @submit.prevent="saveChanges">
      <div class="form-group text-start mb-1">
        <label for="name">Name:</label>
        <input
          v-model="bookData.name"
          type="text"
          class="form-control item"
          id="name"
          placeholder="Name"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="content">Content:</label>
        <input
          v-model="bookData.content"
          type="text"
          class="form-control item"
          id="content"
          placeholder="Content"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="author">Author:</label>
        <input
          v-model="bookData.author"
          type="text"
          class="form-control item"
          id="author"
          placeholder="Author"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="count">Count:</label>
        <input
          v-model="bookData.count"
          type="number"
          class="form-control item"
          id="count"
          placeholder="Count"
        />
      </div>
      <div class="form-group text-start mb-1">
        <label for="price">Price:</label>
        <input
          v-model="bookData.price"
          type="number"
          class="form-control item"
          id="price"
          placeholder="Price"
        />
      </div>
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

export default {
  name: "AddBookForm",
  data() {
    return {
      bookData: {
        name: "",
        content: "",
        author: "",
        count: 0,
        available: true,
        price: 0,
      },
    };
  },
  methods: {
    async saveChanges() {
      try {
        // Check if user role is librarian
        if (this.userRole !== "librarian") {
          alert("Only librarians can add books");
          return;
        }

        // Get access token from localStorage
        const accessToken = localStorage.getItem("accessToken");

        // Proceed with adding book if user is a librarian
        const response = await axios.post(
          "http://127.0.0.1:5000/add-book",
          this.bookData,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`, // Include access token in the request headers
            },
          }
        );
        console.log(response.data);
        // Optionally, you can show a success message or redirect the user after successful addition
      } catch (error) {
        console.error("Error adding book:", error);
        // Handle error - e.g., show an error message to the user
      }
    },
  },
  computed: {
    userRole() {
      const role = localStorage.getItem("role");

      if (!role) {
        return null; // Or any default value as per your application logic
      }
      return role; // Assuming 'role' is the key containing the user's role in the token payload
    },
  },
};
</script>

<style>
body {
  background-color: #dee9ff;
}

.registration-form {
  padding: 50px 0;
}

.registration-form form {
  background-color: #fff;
  max-width: 600px;
  margin: auto;
  padding: 50px 70px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.registration-form .form-icon {
  text-align: center;
  background-color: #5891ff;
  border-radius: 50%;
  font-size: 40px;
  color: white;
  width: 100px;
  height: 100px;
  margin: auto;
  margin-bottom: 50px;
  line-height: 100px;
}

.registration-form .item {
  border-radius: 20px;
  margin-bottom: 25px;
  padding: 10px 20px;
}

.registration-form .create-account {
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 18px;
  font-weight: bold;
  background-color: #5791ff;
  border: none;
  color: white;
  margin-top: 20px;
}

.registration-form .social-media {
  max-width: 600px;
  background-color: #fff;
  margin: auto;
  padding: 35px 0;
  text-align: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
  color: #9fadca;
  border-top: 1px solid #dee9ff;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.075);
}

.registration-form .social-icons {
  margin-top: 30px;
  margin-bottom: 16px;
}

.registration-form .social-icons a {
  font-size: 23px;
  margin: 0 3px;
  color: #5691ff;
  border: 1px solid;
  border-radius: 50%;
  width: 45px;
  display: inline-block;
  height: 45px;
  text-align: center;
  background-color: #fff;
  line-height: 45px;
}

.registration-form .social-icons a:hover {
  text-decoration: none;
  opacity: 0.6;
}

@media (max-width: 576px) {
  .registration-form form {
    padding: 50px 20px;
  }

  .registration-form .form-icon {
    width: 70px;
    height: 70px;
    font-size: 30px;
    line-height: 70px;
  }
}
</style>
