<template>
  <div class="parent-div">
    <Navbar />
    <div class="main-page">
      <UserDetail :username="username" />
      <BooksAvailable :books="books" :heading="booksAvailable" />
      <BooksAvailable :books="requestedBooks" :heading="booksRequested" />
      <BooksAvailable :books="issuedBooks" :heading="booksIssued" />
    </div>
  </div>
</template>

<script>
import Navbar from "./Navbar.vue";
import NewArrival from "./NewArrival.vue";
import BookIssued from "./BookIssued.vue";
import BookRequested from "./BookRequested.vue";
import BookReturned from "./BookReturned.vue";
import BooksAvailable from "./BooksAvailable.vue";
import UserDetail from "./UserDetail.vue";

import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "LandingPage",
  components: {
    Navbar,
    UserDetail,
    BookIssued,
    BookRequested,
    BookReturned,
    BooksAvailable,
    NewArrival,
  },
  data() {
    return {
      username: "", // Initialize username as an empty string
      books: [],
      requestedBooks: [],
      issuedBooks: [],
      booksAvailable: "Books Available",
      booksRequested: "Books Requested",
      booksIssued: "Books Issued",
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      const accessToken = localStorage.getItem("accessToken");

      if (!accessToken) {
        console.error("Access token not found in localStorage");
        return;
      }

      const decodedToken = jwtDecode(accessToken);
      const user_id = decodedToken.sub;

      try {
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

      try {
        // Fetch books
        const booksResponse = await axios.get(`http://127.0.0.1:5000/books`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.books = booksResponse.data; // Assign directly to this.books
        console.log(this.books);
      } catch (error) {
        console.error("Error fetching books:", error);
      }

      try {
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

      try {
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
