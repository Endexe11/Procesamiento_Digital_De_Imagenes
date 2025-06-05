// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyClnvmllAzCH_yWSkwuIQpi4FBHmphD_zg",
  authDomain: "proyecto-procesamiento-digital.firebaseapp.com",
  projectId: "proyecto-procesamiento-digital",
  storageBucket: "proyecto-procesamiento-digital.firebasestorage.app",
  messagingSenderId: "905435001456",
  appId: "1:905435001456:web:5d8df648dc1f8327d83ab5",
  measurementId: "G-D8FG1NTGK5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);