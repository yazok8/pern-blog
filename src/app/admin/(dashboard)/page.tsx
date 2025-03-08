
//src/app/admin/(dashboard)

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Container from '@/app/admin/components/container';

import React from 'react';  
  
export default function AdminPage() {  
  return (  
   <Container className="flex justify-center items-center">  
    <Card className='border-none px-8 py-0'>
      <CardHeader>
        <CardTitle>Admin Dashboard Overview</CardTitle>
      </CardHeader>
      <CardContent>
      </CardContent>
    </Card>
   </Container>  
  );  
}
