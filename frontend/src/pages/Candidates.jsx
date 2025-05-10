import { useState } from 'react'
import { Link } from 'react-router-dom'
import { HiFilter, HiPlus, HiSearch, HiBadgeCheck, HiX } from 'react-icons/hi'

const candidates = [
  { 
    id: 1, 
    name: 'John Doe', 
    email: 'john.doe@example.com',
    position: 'Frontend Developer', 
    experience: 5.5,
    skills: ['React', 'JavaScript', 'TypeScript', 'CSS'],
    source: 'LinkedIn', 
    matchScore: 92, 
    status: 'contacted',
    date: '2 days ago' 
  },
  { 
    id: 2, 
    name: 'Jane Smith', 
    email: 'jane.smith@example.com',
    position: 'UI/UX Designer', 
    experience: 4,
    skills: ['Figma', 'UI Design', 'Wireframing', 'Prototyping'],
    source: 'Applied', 
    matchScore: 88, 
    status: 'new',
    date: '3 days ago' 
  },
  { 
    id: 3, 
    name: 'Michael Johnson', 
    email: 'michael.johnson@example.com',
    position: 'Backend Developer', 
    experience: 7,
    skills: ['Node.js', 'Python', 'MongoDB', 'SQL'],
    source: 'CV Library', 
    matchScore: 85, 
    status: 'interview_scheduled',
    date: '5 days ago' 
  },
  { 
    id: 4, 
    name: 'Priya Patel', 
    email: 'priya.patel@example.com',
    position: 'Full Stack Developer', 
    experience: 3.5,
    skills: ['React', 'Node.js', 'JavaScript', 'SQL'],
    source: 'Naukri', 
    matchScore: 81, 
    status: 'new',
    date: '1 week ago' 
  },
  { 
    id: 5, 
    name: 'Robert Fox', 
    email: 'robert.fox@example.com',
    position: 'Product Manager', 
    experience: 6,
    skills: ['Product Strategy', 'Agile', 'User Research', 'Roadmapping'],
    source: 'LinkedIn', 
    matchScore: 78, 
    status: 'interview_scheduled',
    date: '1 week ago' 
  },
]

const getStatusLabel = (status) => {
  switch (status) {
    case 'new':
      return { text: 'New', color: 'bg-blue-100 text-blue-800' }
    case 'contacted':
      return { text: 'Contacted', color: 'bg-yellow-100 text-yellow-800' }
    case 'interview_scheduled':
      return { text: 'Interview Scheduled', color: 'bg-green-100 text-green-800' }
    case 'hired':
      return { text: 'Hired', color: 'bg-green-100 text-green-800' }
    case 'rejected':
      return { text: 'Rejected', color: 'bg-red-100 text-red-800' }
    default:
      return { text: status, color: 'bg-gray-100 text-gray-800' }
  }
}

export default function Candidates() {
  const [filters, setFilters] = useState([])
  const [searchQuery, setSearchQuery] = useState('')

  const addFilter = (type, value) => {
    if (!filters.some(f => f.type === type && f.value === value)) {
      setFilters([...filters, { type, value }])
    }
  }

  const removeFilter = (index) => {
    setFilters(filters.filter((_, i) => i !== index))
  }

  const clearFilters = () => {
    setFilters([])
    setSearchQuery('')
  }

  return (
    <div>
      <div className="mb-6 sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Candidates</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage and track your candidate pipeline
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Link
            to="/candidates/upload"
            className="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            <HiPlus className="-ml-0.5 mr-2 h-4 w-4" aria-hidden="true" />
            Add Candidate
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white shadow rounded-lg mb-6">
        <div className="p-4 sm:p-6 flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
          <div className="relative flex-grow">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <HiSearch className="h-5 w-5 text-gray-400" aria-hidden="true" />
            </div>
            <input
              type="text"
              className="block w-full rounded-md border-gray-300 pl-10 focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              placeholder="Search candidates..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex-shrink-0">
            <div className="relative">
              <button
                type="button"
                className="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              >
                <HiFilter className="-ml-1 mr-2 h-5 w-5 text-gray-400" aria-hidden="true" />
                Filter
              </button>
            </div>
          </div>
        </div>

        {/* Applied filters */}
        {filters.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 px-4 sm:px-6 pb-4">
            <span className="text-sm font-medium text-gray-700">Filters:</span>
            {filters.map((filter, index) => (
              <span
                key={index}
                className="inline-flex items-center rounded-full bg-gray-100 px-3 py-0.5 text-sm font-medium text-gray-800"
              >
                {filter.type}: {filter.value}
                <button
                  type="button"
                  className="ml-1.5 inline-flex h-4 w-4 flex-shrink-0 items-center justify-center rounded-full text-gray-500 hover:bg-gray-200 hover:text-gray-700 focus:outline-none"
                  onClick={() => removeFilter(index)}
                >
                  <span className="sr-only">Remove filter</span>
                  <HiX className="h-3 w-3" aria-hidden="true" />
                </button>
              </span>
            ))}
            <button
              type="button"
              className="text-sm text-primary-600 hover:text-primary-800"
              onClick={clearFilters}
            >
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Candidates Table */}
      <div className="overflow-hidden bg-white shadow sm:rounded-lg">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="py-3.5 pl-6 pr-3 text-left text-sm font-semibold text-gray-900">
                  Name
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Position
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Experience
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Skills
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Source
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Match
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Status
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Added
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {candidates.map((candidate) => (
                <tr key={candidate.id} className="hover:bg-gray-50">
                  <td className="whitespace-nowrap py-4 pl-6 pr-3 text-sm">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-10 w-10 flex items-center justify-center rounded-full bg-primary-100 text-primary-700">
                          {candidate.name.charAt(0)}
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="font-medium text-gray-900">
                          <Link to={`/candidates/${candidate.id}`} className="hover:text-primary-600">
                            {candidate.name}
                          </Link>
                        </div>
                        <div className="text-gray-500">{candidate.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-900">
                    {candidate.position}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-900">
                    {candidate.experience} years
                  </td>
                  <td className="px-3 py-4 text-sm text-gray-500 max-w-xs">
                    <div className="flex flex-wrap gap-1">
                      {candidate.skills.slice(0, 3).map((skill, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center rounded-full bg-primary-50 px-2 py-0.5 text-xs font-medium text-primary-700"
                        >
                          {skill}
                        </span>
                      ))}
                      {candidate.skills.length > 3 && (
                        <span className="inline-flex items-center rounded-full bg-gray-50 px-2 py-0.5 text-xs font-medium text-gray-600">
                          +{candidate.skills.length - 3} more
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-900">
                    {candidate.source}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-900">
                    <div className="flex items-center">
                      <span 
                        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                          candidate.matchScore >= 90 ? 'bg-green-100 text-green-800' :
                          candidate.matchScore >= 80 ? 'bg-green-50 text-green-700' :
                          candidate.matchScore >= 70 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {candidate.matchScore}%
                      </span>
                      {candidate.matchScore >= 90 && (
                        <HiBadgeCheck className="ml-1 h-5 w-5 text-green-500" aria-hidden="true" />
                      )}
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm">
                    <span
                      className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                        getStatusLabel(candidate.status).color
                      }`}
                    >
                      {getStatusLabel(candidate.status).text}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {candidate.date}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
} 