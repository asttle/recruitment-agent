import { HiUserGroup, HiBriefcase, HiClock, HiCheck } from 'react-icons/hi'
import { Link } from 'react-router-dom'

const stats = [
  { name: 'Total Candidates', value: '248', icon: HiUserGroup, color: 'bg-blue-500' },
  { name: 'Open Jobs', value: '12', icon: HiBriefcase, color: 'bg-green-500' },
  { name: 'Pending Interviews', value: '36', icon: HiClock, color: 'bg-yellow-500' },
  { name: 'Hired', value: '16', icon: HiCheck, color: 'bg-purple-500' },
]

const recentCandidates = [
  { id: 1, name: 'John Doe', position: 'Frontend Developer', source: 'LinkedIn', matchScore: 92, date: '2 days ago' },
  { id: 2, name: 'Jane Smith', position: 'UI/UX Designer', source: 'Applied', matchScore: 88, date: '3 days ago' },
  { id: 3, name: 'Michael Johnson', position: 'Backend Developer', source: 'CV Library', matchScore: 85, date: '5 days ago' },
  { id: 4, name: 'Priya Patel', position: 'Full Stack Developer', source: 'Naukri', matchScore: 81, date: '1 week ago' },
]

const upcomingInterviews = [
  { id: 1, candidate: 'Robert Fox', position: 'Product Manager', date: 'Today at 2:00 PM' },
  { id: 2, candidate: 'Esther Howard', position: 'Data Scientist', date: 'Tomorrow at 10:00 AM' },
  { id: 3, candidate: 'Jenny Wilson', position: 'Backend Developer', date: 'Aug 15, 11:30 AM' },
]

export default function Dashboard() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your recruitment pipeline
        </p>
      </div>

      {/* Stats grid */}
      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="overflow-hidden rounded-lg bg-white shadow"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 rounded-md p-3 ${stat.color}`}>
                  <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{stat.name}</dt>
                    <dd>
                      <div className="text-lg font-medium text-gray-900">{stat.value}</div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Candidates */}
        <div className="overflow-hidden rounded-lg bg-white shadow">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium text-gray-900">Recent Candidates</h2>
              <Link to="/candidates" className="text-sm font-medium text-primary-600 hover:text-primary-800">
                View all
              </Link>
            </div>
            <div className="mt-6 flow-root">
              <ul className="-my-5 divide-y divide-gray-200">
                {recentCandidates.map((candidate) => (
                  <li key={candidate.id} className="py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-primary-700">
                            {candidate.name.charAt(0)}
                          </div>
                        </div>
                        <div className="ml-4">
                          <h3 className="text-sm font-medium text-gray-900">{candidate.name}</h3>
                          <p className="text-xs text-gray-500">{candidate.position}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
                          {candidate.matchScore}% match
                        </div>
                        <p className="mt-1 text-xs text-gray-500">{candidate.source} • {candidate.date}</p>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Upcoming Interviews */}
        <div className="overflow-hidden rounded-lg bg-white shadow">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium text-gray-900">Upcoming Interviews</h2>
              <button className="text-sm font-medium text-primary-600 hover:text-primary-800">
                View calendar
              </button>
            </div>
            <div className="mt-6 flow-root">
              <ul className="-my-5 divide-y divide-gray-200">
                {upcomingInterviews.map((interview) => (
                  <li key={interview.id} className="py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-yellow-100 text-yellow-700">
                            {interview.candidate.charAt(0)}
                          </div>
                        </div>
                        <div className="ml-4">
                          <h3 className="text-sm font-medium text-gray-900">{interview.candidate}</h3>
                          <p className="text-xs text-gray-500">{interview.position}</p>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="flex items-center text-sm font-medium text-gray-900">
                          <HiClock className="mr-1.5 h-5 w-5 flex-shrink-0 text-gray-400" />
                          {interview.date}
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 