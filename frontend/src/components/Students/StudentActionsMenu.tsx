import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { StudentPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteStudent from "../Students/DeleteStudent"
import EditStudent from "../Students/EditStudent"

interface StudentActionsMenuProps {
  student: StudentPublic
}

export const StudentActionsMenu = ({ student }: StudentActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditStudent student={student} onSuccess={() => setOpen(false)} />
        <DeleteStudent id={student.id} onSuccess={() => setOpen(false)} />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
