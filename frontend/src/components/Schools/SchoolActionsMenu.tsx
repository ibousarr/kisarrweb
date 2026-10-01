import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { SchoolPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteSchool from "../Schools/DeleteSchool"
import EditSchool from "../Schools/EditSchool"

interface SchoolActionsMenuProps {
  school: SchoolPublic
}

export const SchoolActionsMenu = ({ school }: SchoolActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditSchool school={school} onSuccess={() => setOpen(false)} />
        <DeleteSchool id={school.id} onSuccess={() => setOpen(false)} />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
