export const getDbConnectionString = () => {
    return process.env.MONGO_DB_CONNECTION_STRING!;
}