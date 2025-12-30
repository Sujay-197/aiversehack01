
import NextAuth from "next-auth"
import GitHub from "next-auth/providers/github"
import Credentials from "next-auth/providers/credentials"

export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: [
        GitHub({
            clientId: process.env.GITHUB_ID,
            clientSecret: process.env.GITHUB_SECRET,
        }),
        Credentials({
            name: "Debug Login",
            credentials: {
                email: { label: "Email", type: "text", placeholder: "debug@example.com" },
            },
            async authorize(credentials) {
                if (!credentials?.email) return null;

                return {
                    id: "debug-user",
                    name: "Debug Researcher",
                    email: credentials.email as string,
                    image: "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                }
            }
        })
    ],
    pages: {
        signIn: "/",
    },
    secret: process.env.NEXTAUTH_SECRET || "fallback_secret_for_dev",
    debug: process.env.NODE_ENV === "development",
})
