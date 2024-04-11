<template>
  <div class="parent-div">
    <Navbar />
    <div class="main-page">
      <UserDetail :username="username" :userId="user_id" />
      <BooksAvailable :books="books" :heading="booksAvailable" />
      <BooksAvailable :books="requestedBooks" :heading="booksRequested" />
      <BooksAvailable :books="issuedBooks" :heading="booksIssued" />
    </div>
  </div>
</template>

<script>
import BooksAvailable from "@/components/BooksAvailable.vue";
import Navbar from "@/components/Navbar.vue";
import UserDetail from "@/components/UserDetail.vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "LandingPage",
  props: ["roleRequired"],
  components: {
    Navbar,
    UserDetail,
    BooksAvailable,
  },
  data() {
    return {
      username: "", // Initialize username as an empty string
      user_id: null, // Initialize user_id as null
      books: [],
      requestedBooks: [],
      issuedBooks: [],
      booksAvailable: "Books Available",
      booksRequested: "Books Requested",
      booksIssued: "Books Issued",
    };
  },
  mounted() {
    const accessToken = localStorage.getItem("accessToken");

    if (!accessToken) {
      console.error("Access token not found in localStorage");
      // Redirect to login page or handle the absence of token
      return;
    }

    const decodedToken = jwtDecode(accessToken);
    const user_id = decodedToken.sub;

    // Set user_id to the component data
    this.user_id = user_id;

    // Fetch user information if the role matches
    this.fetchUserInfo(user_id);
  },
  methods: {
    async fetchUserInfo(user_id) {
      try {
        const accessToken = localStorage.getItem("accessToken");

        const userInfoResponse = await axios.get(
          `http://127.0.0.1:5000/user-info/${user_id}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.username = userInfoResponse.data.username;
      } catch (error) {
        console.error("Error fetching user info:", error);
      }

      // Fetch other data using user_id
      this.fetchBooks(user_id);
      this.fetchRequestedBooks(user_id);
      this.fetchIssuedBooks(user_id);
    },
    async fetchBooks(user_id) {
      try {
        const accessToken = localStorage.getItem("accessToken");

        const booksResponse = await axios.get(`http://127.0.0.1:5000/books`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.books = booksResponse.data; // Assign directly to this.books
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    },
    async fetchRequestedBooks(user_id) {
      try {
        const accessToken = localStorage.getItem("accessToken");

        const requestedBooksResponse = await axios.get(
          `http://127.0.0.1:5000/requested-books/${user_id}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.requestedBooks = requestedBooksResponse.data;
      } catch (error) {
        console.error("Error fetching requested books:", error);
      }
    },
    async fetchIssuedBooks(user_id) {
      try {
        const accessToken = localStorage.getItem("accessToken");

        const issuedBooksResponse = await axios.get(
          `http://127.0.0.1:5000/issued-books/${user_id}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.issuedBooks = issuedBooksResponse.data;
      } catch (error) {
        console.error("Error fetching issued books:", error);
      }
    },
  },
};
</script>

<style scoped>
.parent-div {
  display: flex;
  flex-direction: column;
  padding: 0 2rem;
  gap: 2rem;
}
.main-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>
