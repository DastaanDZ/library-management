<template>
  <div class="parent-div">
    <div class="main-page">
      <UserDetail :username="username" />
      <BooksAvailable :books="books" :heading="booksAvailable" />
      <BooksAvailable :books="requestedBooks" :heading="booksRequested" />
      <BooksAvailable :books="issuedBooks" :heading="booksIssued" />
    </div>
  </div>
</template>

<script>
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
  props: ["roleRequired"],
  components: {
    UserDetail,
    BookIssued,
    BookRequested,
    BookReturned,
    BooksAvailable,
    NewArrival,
  },
  data() {
    return {
      username: "",
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
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
      }

      try {
        // Fetch books
        const booksResponse = await axios.get(`http://127.0.0.1:5000/books`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.books = booksResponse.data;
        console.log(this.books);
      } catch (error) {
        console.error("Error fetching books:", error);
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
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
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
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
        if (error.response && error.response.status === 401) {
          this.$router.push("/login");
        }
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
