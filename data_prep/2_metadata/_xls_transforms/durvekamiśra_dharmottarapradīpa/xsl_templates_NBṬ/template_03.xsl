<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="quote[@type='commentary1']">
<quote>
<xsl:copy-of select="./@*"/>
<xsl:attribute name="section">
<xsl:value-of select="descendant::quote[@type='base-text']/@n"/>
</xsl:attribute>
<xsl:copy-of select="./node()"/>
</quote>
</xsl:template>

</xsl:stylesheet>
