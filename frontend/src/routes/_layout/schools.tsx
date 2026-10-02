/** biome-ignore-all assist/source/organizeImports: <explanation> */
import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { SchoolsService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddSchool from "@/components/Schools/AddSchool"
import { columns } from "@/components/Schools/columns"
import PendingSchools from "@/components/Pending/PendingSchools"

function getSchoolsQueryOptions() {
  return {
    queryFn: async () =>
      (await SchoolsService.readSchools({ query: { skip: 0, limit: 100 } }))
        .data,
    queryKey: ["schools"],
  }
}

export const Route = createFileRoute("/_layout/schools")({
  component: Schools,
  head: () => ({
    meta: [
      {
        title: "Schools - Kisarr Web",
      },
    ],
  }),
})

function SchoolsTableContent() {
  const { data: schools } = useSuspenseQuery(getSchoolsQueryOptions())

  if (schools.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any schools yet
        </h3>
        <p className="text-muted-foreground">Add a new school to get started</p>
      </div>
    )
  }

  return <DataTable columns={columns} data={schools.data} />
}

function SchoolsTable() {
  return (
    <Suspense fallback={<PendingSchools />}>
      <SchoolsTableContent />
    </Suspense>
  )
}

function Schools() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Schools</h1>
          <p className="text-muted-foreground">
            Create and manage your schools
          </p>
        </div>
        <AddSchool />
      </div>
      <SchoolsTable />
    </div>
  )
}
