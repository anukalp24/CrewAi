import React, { useState } from "react";
import "./Auth.css";
import banner from "../../../assets/CrewAi_auth_banner.png";

const Auth = () => {
  const [IsSignup, setIsSignup] = useState(true);

const [data, setdata] = useState({
name: "",
email: "",
password: ""
})

const [error, seterror] = useState("")




  const handleAuth = async (e)=>{

    e.preventDefault()
seterror("")
const passwordRegex =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^_+-])[A-Za-z\d@$!%*?&#^_+-]{8,}$/;


    if(IsSignup){

      if(data.password){

        if(!passwordRegex.test(data.password)){
          return seterror("Password must be at least 8 characters and include uppercase, lowercase, a number, and a special character.")
        }
      }
const req = await fetch("http://127.0.0.1:8000/signin" , {
  headers: { "Content-Type": "application/json" },
method: "POST",
body: JSON.stringify(data)
      })
      




    }



    else{
      const req = await fetch("http://127.0.0.1:8000/login" , {
  headers: { "Content-Type": "application/json" },
method: "POST",
body: JSON.stringify(data)
    })


    
  }
  }


  const handlechange = (e)=>{
    setdata({... data , [e.target.name] : e.target.value})
  }
  return (
    <main className="auth-page">

      {/* LEFT — PRODUCT VISUAL */}

      <section className="auth-visual">

        <img
          src={banner}
          alt=""
          className="auth-visual-image"
        />

        <div className="auth-visual-overlay">

          <div className="auth-brand">
            <span className="auth-brand-mark">✦</span>
            <span>CrewAi</span>
          </div>

        </div>

      </section>


      {/* RIGHT — AUTHENTICATION */}

      <section className="auth-content">

        {IsSignup ? (

          /* SIGNUP */

          <div className="auth-box">

            <div className="auth-header">

              <span className="auth-eyebrow">
                GET STARTED
              </span>

              <h1>
                Create your
                <span> CrewAi account.</span>
              </h1>

            </div>


            <form onSubmit={handleAuth} className="auth-form">

              <div className="auth-field">

                <label htmlFor="signup-name">
                  Full name
                </label>

                <input name="name"  onChange={handlechange}
                  id="signup-name"
                  type="text"
                  placeholder="Your name"
                  autoComplete="name"
                  required
                />

              </div>


              <div className="auth-field">

                <label htmlFor="signup-email">
                  Email
                </label>

                <input name="email" onChange={handlechange}
                  id="signup-email"
                  type="email"
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                />

              </div>


              <div className="auth-field">

                <label htmlFor="signup-password">
                  Password
                </label>

                <input name="password" onChange={handlechange}
                  id="signup-password"
                  type="password"
                  placeholder="Create a password"
                  autoComplete="new-password"
                  required
                />

                {error && (
                  <p>{error}</p>
                )}


              </div>


              <button 
                type="submit"
                className="auth-submit"
              >
                Create account
                <span>→</span>
              </button>

            </form>


            <div className="auth-divider">
              <span>OR</span>
            </div>


            <button
              type="button"
              className="auth-github"
            >
              <span className="auth-github-icon">◉</span>
              Continue with GitHub
            </button>


            <p className="auth-switch">
              Already have an account?

              <a
                onClick={(e)=> {setIsSignup(false) ; setdata({}) ; e.preventDefault()}}
              >
                {" "}Log in
              </a>
            </p>

          </div>

        ) : (

          /* LOGIN */

          <div className="auth-box">

            <div className="auth-header">

              <span className="auth-eyebrow">
                WELCOME BACK
              </span>

              <h1>
                Log in to
                <span> CrewAi.</span>
              </h1>

            </div>


            <form onSubmit={handleAuth} className="auth-form">

              <div className="auth-field">

                <label htmlFor="login-email">
                  Email
                </label>

                <input name="email" onChange={handlechange}
                  id="login-email"
                  type="email"
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                />

              </div>


              <div className="auth-field">

                <div className="auth-password-label">

                  <label htmlFor="login-password">
                    Password
                  </label>

                  <a href="/forgot-password">
                    Forgot password?
                  </a>

                </div>

                <input name="password" onChange={handlechange}
                  id="login-password"
                  type="password"
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                />

                {error && (
                  <p>{error}</p>
                )}

              </div>


              <button 
                type="submit"
                className="auth-submit"
              >
                Log in
                <span>→</span>
              </button>

            </form>


            <div className="auth-divider">
              <span>OR</span>
            </div>


            <button
              type="button"
              className="auth-github"
            >
              <span className="auth-github-icon">◉</span>
              Continue with GitHub
            </button>


            <p className="auth-switch">
              Don't have an account?

              <a
                href="/signup"
                onClick={(e) => {
                  e.preventDefault();
                  setIsSignup(true);
                  setdata({})
                }}
              >
                {" "}Create one
              </a>
            </p>

          </div>

        )}


        <p className="auth-legal">
          By continuing, you agree to CrewAi's{" "}
          <a href="/terms">Terms</a> and{" "}
          <a href="/privacy">Privacy Policy</a>.
        </p>

      </section>

    </main>
  );

}
export default Auth;