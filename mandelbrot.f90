subroutine generate_heat_map(matrix,min_x,min_y,i_n,j_n,abs_x,abs_y,max_iteration)

    !====================================================
    ! Generates the mandelbrot set in the range of given
    ! coordinates and with resolution n
    !====================================================
    implicit none 
    integer, parameter :: k=8
    real    (kind=k), intent(in)  :: min_x,min_y
    integer (kind=k), intent(in)  :: i_n,j_n,max_iteration
    integer (kind=k), intent(out) :: matrix(i_n,j_n)
    complex (kind=k) :: z,z_0
    real    (kind=k) :: abs_x,abs_y
    integer (kind=k) :: i,j
    integer (kind=k) :: count

    !$omp parallel shared(i_n,j_n,min_x,min_y,abs_x,abs_y,matrix) private(i,j,count,z_0,z)
    !$omp do ordered
    do i=0,i_n-1
        do j=0,j_n-1
             
            count=0                                                         
            z = 0                                                          
            z_0 = complex(i*abs_x/i_n+min_x,(j*abs_y/j_n-min_y)*(-1))
            do while (abs(z) < 2 .and. count < max_iteration)
                z = z*z + z_0
                count = count + 1
            end do

            matrix(i+1,j+1) = count
        end do
    end do
    !$omp end do
    !$omp end parallel    

end subroutine generate_heat_map