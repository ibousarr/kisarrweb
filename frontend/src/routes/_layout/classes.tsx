/** biome-ignore-all assist/source/organizeImports: <explanation> */
import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { ClassesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddClasse from "@/components/Classes/AddClasse"
import { columns } from "@/components/Classes/columns"
import PendingClasses from "@/components/Pending/PendingClasses"

function getClassesQueryOptions() {
  return {
    queryFn: async () =>
      (await ClassesService.readClasses({ query: { skip: 0, limit: 100 } }))
        .data,
    queryKey: ["classes"],
  }
}

export const Route = createFileRoute("/_layout/classes")({
  component: Classes,
  head: () => ({
    meta: [
      {
        title: "Classes - Kisarr Web",
      },
    ],
  }),
})

function ClassesTableContent() {
  const { data: classes } = useSuspenseQuery(getClassesQueryOptions())

  if (classes.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any classes yet
        </h3>
        <p className="text-muted-foreground">Add a new Classe to get started</p>
      </div>
    )
  }

  return <DataTable columns={columns} data={classes.data} />
}

function ClassesTable() {
  return (
    <Suspense fallback={<PendingClasses />}>
      <ClassesTableContent />
    </Suspense>
  )
}

function Classes() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Classes</h1>
          <p className="text-muted-foreground">
            Create and manage your Classes
          </p>
        </div>
        <AddClasse />
      </div>
      <ClassesTable />
    </div>
  )
}
