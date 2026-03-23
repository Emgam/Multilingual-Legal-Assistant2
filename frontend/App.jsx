

import { useState } from "react";
import SignIn from "./SignIn";
import SignUp from "./SignUp";
import Chat from "./Chat";

/**
 * StartupTN - AI Assistant for Tunisian Startup & CNSS Procedures
 *
 * Pages:
 *   signin  → Sign In page
 *   signup  → Sign Up page
 *   chat    → Chat interface
 *
 * Shared state (hoisted here so it persists across page changes):
 *   lang    → "en" | "fr" | "dar"
 *   dark    → boolean
 */
export default function App() {
    const [page, setPage] = useState("signin"); // "signin" | "signup" | "chat"
    const [lang, setLang] = useState("en");
    const [dark, setDark] = useState(false);

    const sharedProps = {
        lang,
        setLang,
        dark,
        toggleDark: () => setDark((d) => !d),
        onNavigate: setPage,
    };

    return (
        <>
            {page === "signin" && <SignIn {...sharedProps} />}
            {page === "signup" && <SignUp {...sharedProps} />}
            {page === "chat" && <Chat  {...sharedProps} />}
        </>
    );
}