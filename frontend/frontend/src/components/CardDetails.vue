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
          <div class="card-body">
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
            <!-- Show buttons based on user role and book status -->
            <div v-if="userRole === 'user' && !bookIssued">
              <button @click="requestBook" class="btn btn-primary">
                Request Book
              </button>
            </div>
            <div v-else>
              <button class="btn btn-secondary" disabled>
                Book Already Requested
              </button>
            </div>
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
      userRole: null,
      bookIssued: false,
      user_id: null, // Added user_id to data
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

    this.bookIssued = requestedBooks.some(
      (book) => book.book_id === parseInt(this.book_id)
    );
    console.log("BOOK REQUESTED", this.bookIssued);

    await this.fetchBookDetails();
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

        this.book = response.data; // Corrected from book to this.book
        console.log("BOOK", this.book); // Corrected from book to this.book
        console.log(this.book);
      } catch (error) {
        console.error("Error fetching book details:", error);
      }
    },
    // async getUserRequestedBooks() {
    //   try {
    //     const accessToken = localStorage.getItem("accessToken");

    //     const response = await axios.get(
    //       `http://127.0.0.1:5000/requested-books/${this.user_id}`,
    //       {
    //         headers: {
    //           Authorization: `Bearer ${accessToken}`,
    //         },
    //       }
    //     );

    //     const requestedBooks = response.data;

    //     requestedBooks.map((book) => {
    //       console.log("Book:", book);
    //       console.log("ID:", book.id);
    //       console.log("Name:", book.name);
    //       console.log("Author:", book.author);
    //       console.log("Price:", book.price);
    //       // Add more properties as needed
    //     });

    //     this.bookIssued = requestedBooks.some(
    //       (book) => book.book_id === parseInt(this.book_id)
    //     );
    //     console.log("BOOK REQUESTED", this.bookIssued);
    //   } catch (error) {
    //     console.error("Error fetching user requested books:", error);
    //   }
    // },
  },
};
</script>
