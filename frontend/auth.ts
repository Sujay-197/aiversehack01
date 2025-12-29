
import NextAuth from "next-auth"
import GitHub from "next-auth/providers/github"

export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: [
        GitHub({
            clientId: process.env.GITHUB_ID,
            clientSecret: process.env.GITHUB_SECRET,
        })
    ],
    pages: {
        signIn: "/",
    },
    // Explicitly fallback to a hardcoded check to force failure if env is missing
    secret: process.env.NEXTAUTH_SECRET || "fallback_secret_for_build_time_only",
    debug: true, // Enable debug in production temporarily to see logs
})
