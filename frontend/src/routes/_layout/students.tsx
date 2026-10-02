import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"
import { StudentsService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddStudent from "@/components/Students/AddStudent"
import { columns } from "@/components/Students/columns"
import PendingStudents from "@/components/Pending/PendingStudents"


function getStudentsQueryOptions() {
  return {
    queryFn: async () =>
      (await StudentsService.readStudents({ query: { skip: 0, limit: 100 } }))
        .data,
    queryKey: ["students"],
  }
}

export const Route = createFileRoute('/_layout/students')({
  component: Students,
  head: () => ({
    meta: [
      {
        title: "Students - Kisarr Web",
      },
    ],
  }),
})

function StudentsTableContent() {
  const { data: students } = useSuspenseQuery(getStudentsQueryOptions())

  if (students.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any students yet
        </h3>
        <p className="text-muted-foreground">Add a new student to get started</p>
      </div>
    )
  }

  return <DataTable columns={columns} data={students.data} />
}

function StudentsTable() {
  return (
    <Suspense fallback={<PendingStudents />}>
      <StudentsTableContent />
    </Suspense>
  )
}

function Students() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Students</h1>
          <p className="text-muted-foreground">
            Create and manage your students
          </p>
        </div>
        <AddStudent />
      </div>
      <StudentsTable />
    </div>
  )
}

