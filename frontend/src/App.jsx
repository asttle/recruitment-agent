import { Routes, Route } from 'react-router-dom'
import MainLayout from '@components/layout/MainLayout'
import Dashboard from '@pages/Dashboard'
import Candidates from '@pages/Candidates'
import CandidateDetails from '@pages/CandidateDetails'
import Jobs from '@pages/Jobs'
import JobDetails from '@pages/JobDetails'
import CreateJob from '@pages/CreateJob'
import ExternalSearch from '@pages/ExternalSearch'
import Settings from '@pages/Settings'
import NotFound from '@pages/NotFound'

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="candidates" element={<Candidates />} />
        <Route path="candidates/:id" element={<CandidateDetails />} />
        <Route path="jobs" element={<Jobs />} />
        <Route path="jobs/create" element={<CreateJob />} />
        <Route path="jobs/:id" element={<JobDetails />} />
        <Route path="search" element={<ExternalSearch />} />
        <Route path="settings" element={<Settings />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}

export default App 