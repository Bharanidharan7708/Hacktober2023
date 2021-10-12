var number = 8
if(number == 0)
{
    console.log("This number is not a power of 2")
}
else if(((number) & (number-1)) == 0)
{
    console.log("This number is  a power of 2")
}
else
{
    console.log("This number is not a power of 2")
}
