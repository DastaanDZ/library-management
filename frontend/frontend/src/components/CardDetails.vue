<template>
  <div
    class="h-100 d-flex justify-content-center align-items-center min-vh-100"
  >
    <div v-if="book" class="card mb-3" style="max-width: 900px">
      <div class="row g-0">
        <div class="col-md-4">
          <img
            src="./book.jpg"
            class="img-fluid rounded-start"
            alt="Book Cover"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body text-start">
            <h5>Name</h5>
            <h5 class="card-title">{{ book.name }}</h5>
            <p>Content</p>
            <p class="card-text">{{ book.content }}</p>
            <p>Author</p>
            <p class="card-text">{{ book.author }}</p>
            <p>Price</p>
            <p class="card-text">{{ book.price }}</p>
            <p class="card-text">
              <small class="text-muted"
                >Last updated: {{ book.lastUpdated }}</small
              >
            </p>
          </div>
          <div class="btn-group">
            <button
              v-if="!bookExists"
              class="btn btn-primary mt-3"
              type="submit"
              @click="requestBook"
            >
              Request
            </button>

            <button
              v-if="bookIssued"
              class="btn btn-primary mt-3"
              type="submit"
              @click="redirectToFeedbackPage"
            >
              Feedback
            </button>

            <button
              v-if="bookIssued"
              class="btn btn-primary mt-3"
              type="submit"
              @click="returnBook"
            >
              Return
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
  name: "CardDetails",
  props: {
    book_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      book: null,
      bookExists: false,
      bookIssued: false, // Add a new data property to track book existence
    };
  },
  async mounted() {
    // Fetch book details based on the ID prop
    const accessToken = localStorage.getItem("accessToken");
    this.userRole = localStorage.getItem("role");

    if (!accessToken) {
      console.error("Access token not found in localStorage");
      return;
    }

    const decodedToken = jwtDecode(accessToken);
    this.user_id = decodedToken.sub; // Set user_id

    const response = await axios.get(
      `http://127.0.0.1:5000/requested-books/${this.user_id}`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    const requestedBooks = response.data;

    // Check if the current book ID exists in the list of requested books
    this.bookExists = requestedBooks.some(
      (book) => book.book_id === parseInt(this.book_id)
    );

    if (this.bookExists) {
      console.log("BOOK is already requested");
    }

    this.fetchBookDetails();
    this.checkIssuedStatus();
  },
  methods: {
    async fetchBookDetails() {
      const accessToken = localStorage.getItem("accessToken"); // Define accessToken here

      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/books/${this.book_id}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        this.book = response.data;
        console.log("BOOK", this.book);
        console.log(this.book);
      } catch (error) {
        console.error("Error fetching book details:", error);
      }
    },
    async checkIssuedStatus() {
      try {
        // Fetch issued books for the user
        const issuedBooksResponse = await axios.get(
          `http://127.0.0.1:5000/issued-books/${this.user_id}`
        );
        const issuedBooks = issuedBooksResponse.data;
        console.log("ISSUED BOOKS", issuedBooks);
        this.bookIssued = issuedBooks.some(
          (book) => book.book_id == this.book_id
        );
        console.log("ISSUED STATUS", this.bookIssued);
      } catch (error) {
        console.error("Error fetching issued books:", error);
      }
    },
    async requestBook() {
      try {
        const accessToken = localStorage.getItem("accessToken");

        // Send a POST request to the server to request the book
        await axios.post(
          `http://127.0.0.1:5000/request-book/${this.book_id}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        // Update the UI to reflect that the book has been requested
        this.bookExists = true; // Set bookExists to true after requesting the book
        alert("Book requested successfully");
        console.log("Book requested successfully");
      } catch (error) {
        console.error("Error requesting book:", error);
      }
    },
    checkBookAvailability() {
      return this.bookExists; // Return the book existence status
    },
    redirectToFeedbackPage() {
      // Redirect to the feedback page with the book ID
      this.$router.push(`/feedback/${this.book_id}`);
    },
    async returnBook() {
      try {
        const accessToken = localStorage.getItem("accessToken");

        // Send a POST request to the server to return the book
        await axios.post(
          `http://127.0.0.1:5000/return-book/${this.book_id}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        // Update the UI to reflect that the book has been returned
        this.bookExists = false; // Set bookExists to false after returning the book
        alert("Book returned successfully");
        console.log("Book returned successfully");
        this.$router.push(`/user`);
      } catch (error) {
        console.error("Error returning book:", error);
      }
    },
  },
};
</script>
