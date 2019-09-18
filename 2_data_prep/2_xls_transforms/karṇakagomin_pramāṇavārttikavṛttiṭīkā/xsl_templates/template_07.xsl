<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>


<xsl:template match="body/quote[@sameAs or @corresp]">

[<xsl:value-of select="@pb_n"/>,<xsl:value-of select="@pb_n2"/>]

<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>

<xsl:text>(</xsl:text>
<xsl:value-of select="@sameAs"/><xsl:value-of select="@corresp"/>
<xsl:text>)</xsl:text>

</xsl:template>

<xsl:template match="body/quote[not(@sameAs) and not(@corresp)]">

[<xsl:value-of select="@pb_n"/>,<xsl:value-of select="@pb_n2"/>]

<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>

</xsl:template>






<xsl:template match="body/p|body/lg">

[<xsl:value-of select="@pb_n"/>,<xsl:value-of select="@pb_n2"/>]

<xsl:value-of select="."/>
</xsl:template>


<xsl:template match="pb" />

</xsl:stylesheet>