import { Link } from 'react-router-dom'
import { HiHome } from 'react-icons/hi'

export default function NotFound() {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center py-16 px-4 sm:py-24 sm:px-6 lg:px-8">
      <div className="flex flex-col items-center">
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">Page not found</h1>
        <p className="mt-6 text-base leading-7 text-gray-600">Sorry, we couldn't find the page you're looking for.</p>
        <div className="mt-10">
          <Link to="/" className="inline-flex items-center rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
            <HiHome className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            Go back home
          </Link>
        </div>
      </div>
    </div>
  )
} 